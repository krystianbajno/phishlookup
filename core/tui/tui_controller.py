import curses
import idna

class ConsoleController:
    def __init__(self, stdscr, ui_update_queue):
        self.stdscr = stdscr
        self.rows_printed = 2  # Start below the header
        self.processed_text = "Processed 0/0 domains"
        self.results_buffer = []
        self.current_top_row = 0
        self.follow_mode = False  # Default to False to allow manual scrolling
        self.ui_update_queue = ui_update_queue
        self.running = True
        self.initialize_colors()
        self.create_header()

    def initialize_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def create_header(self):
        headers = f"{'Domain':<50} | {'Available':<21} | {'IP Address':<15} | {'GeoLookup':<30} | {'Punycode':<8} | {'WHOIS Status'}"
        separator = "-" * len(headers)
        self.stdscr.addstr(0, 0, headers, curses.A_BOLD)
        self.stdscr.addstr(1, 0, separator)
        self.stdscr.refresh()

    def render(self, result=None, progress=None):
        if result:
            self.add_result_to_buffer(result)
        if progress:
            self.update_progress(progress[0], progress[1])
        self.stdscr.refresh()

    def scroll_to_end(self):
        max_y, _ = self.stdscr.getmaxyx()
        visible_rows = max_y - 4
        self.current_top_row = max(0, len(self.results_buffer) - visible_rows)
        self.render_results()

    def add_result_to_buffer(self, result):
        self.results_buffer.append(result)
        if self.current_top_row > 0:
            self.current_top_row -= 1

        if self.follow_mode:
            self.scroll_to_end()
        self.render_results()

    def render_results(self):
        max_y, max_x = self.stdscr.getmaxyx()
        visible_rows = max_y - 4
        self.clear_result_area(max_y)
        self.display_results(visible_rows)

    def clear_result_area(self, max_y):
        for row in range(2, max_y - 2):
            self.stdscr.move(row, 0)
            self.stdscr.clrtoeol()

    def display_results(self, visible_rows):
        self.rows_printed = 2
        for i, result in enumerate(self.results_buffer[self.current_top_row:self.current_top_row + visible_rows]):
            color = curses.color_pair(2) if result['is_available'] == "AVAILABLE" else curses.color_pair(1)
            decoded_domain = self.decode_domain(result['domain'], result['punycode'])
            try:
                self.stdscr.addstr(self.rows_printed, 0,
                                   f"{decoded_domain:<50} | {result['is_available']:<21} | {result['ip_address']:<15} | {result['geoip']:<30} | {result['punycode']:<8} | {result['whois_status']}",
                                   color)
                self.rows_printed += 1
            except curses.error:
                break

    def decode_domain(self, domain, punycode_status):
        if punycode_status == "Y":
            try:
                return f"{domain} ({idna.encode(domain).decode()})"
            except (idna.IDNAError, UnicodeEncodeError):
                return f"{domain} (decoding error)"
        return domain

    def update_progress(self, processed_count, total_count):
        self.processed_text = f"Processed {processed_count}/{total_count} domains"
        self.display_guide_and_status()

    def display_guide_and_status(self):
        max_y, max_x = self.stdscr.getmaxyx()
        guide_text = "[Q] Quit [Space] Follow [Scroll/Arrows] Up/Down"
        y_pos = max_y - 1
        self.stdscr.addstr(y_pos, 0, self.processed_text)
        self.stdscr.clrtoeol()
        x_pos = max_x - len(guide_text) - 1
        self.stdscr.addstr(y_pos, x_pos, guide_text)

    def handle_input(self):
        self.stdscr.nodelay(True)
        try:
            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                self.scroll_up()
            elif key == curses.KEY_DOWN:
                self.scroll_down()
            elif key == ord(' '):  # Space bar toggles follow mode
                self.toggle_follow_mode()
            elif key == ord('q'):  # 'q' to quit
                self.running = False
        except:
            pass

    def process_queue(self):
        """Handles the updates coming from the queue in the main loop."""
        while not self.ui_update_queue.empty():
            update = self.ui_update_queue.get()
            if update[0] == 'result':
                self.render(result=update[1])
            elif update[0] == 'progress':
                self.render(progress=(update[1], update[2]))
            self.ui_update_queue.task_done()

    def toggle_follow_mode(self):
        """Toggles follow mode when space bar is pressed."""
        self.follow_mode = not self.follow_mode
        if self.follow_mode:
            self.scroll_to_end()

    def scroll_up(self):
        if self.current_top_row > 0:
            self.current_top_row -= 1
            self.follow_mode = False  # Stop following when scrolling manually
            self.render_results()
        else:
            self.display_message("Already at the top.", color_pair=3)

    def scroll_down(self):
        max_y, _ = self.stdscr.getmaxyx()
        visible_rows = max_y - 4
        if self.current_top_row < len(self.results_buffer) - visible_rows:
            self.current_top_row += 1
            self.follow_mode = False  # Stop following when scrolling manually
            self.render_results()
        else:
            self.display_message("Already at the bottom.", color_pair=3)

    def display_message(self, message, color_pair=3):
        max_y, _ = self.stdscr.getmaxyx()
        message_row = max_y - 3
        self.stdscr.move(message_row, 0)
        self.stdscr.clrtoeol()
        self.stdscr.addstr(message_row, 0, message, curses.color_pair(color_pair))
        self.stdscr.refresh()
