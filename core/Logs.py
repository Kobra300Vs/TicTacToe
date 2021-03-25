from core.player.PlayerCircle import PlayerCircle
from core.player.PlayerCross import PlayerCross


class Logs:
    def __init__(self, name_of_player_one, name_of_player_two, p_win_logs):
        """
        :param name_of_player_one: Name of PlayerCircle
        :param name_of_player_two: Name of PlayerCross
        :param p_win_logs: -> player_win_logs - listing logs of winners in rounds
        """
        self.player_circle = PlayerCircle(name_of_player_one)  # I need names of
        self.player_cross = PlayerCross(name_of_player_two)
        self.player_win_logs = p_win_logs

    def logs_with_load(self):
        """
        Load and then saving logs from txt to txt
        :return: none
        """
        last_logs = self.load_logs()
        logs = self.logs()
        try:
            correct_logs = last_logs + logs
        except TypeError:  # I could also check is there file / is empty... but. This is way faster imo.
            correct_logs = logs
        file = open("./logs.txt", 'w', encoding='utf-8')
        for each in correct_logs:
            file.write(each)
        file.close()

    @staticmethod
    def load_logs():
        """
        Loading logs from file and make some basic refactoring
        :return: none IF there is no file ELSE refactor input from logs.txt file
        """
        try:  # trying to get last logs, if file exist, else when I got error I want to return logs as empty
            with open('./logs.txt', 'r') as file:  # it's temporary
                # file = open('logs.txt)  # without "with" this should be a solution
                lines = file.readlines()
                to_pass = []  # list to pass where? to logs, that mean I share content of logs.txt to function
                """for line in lines:
                    if line[0:2] == "In":
                        to_pass += line
                return to_pass
                # This one was only if I want to show only results, not rounds log
                """
                for line in lines:
                    to_pass += line
                # file.close() this is unnecessary with "with", but without is necessary
            return to_pass
        except FileNotFoundError:  # if there is no file with logs = there is no logs to pass
            return ""

    def logs(self):
        """
        Making logs into return list to save it logs.txt later logs_withX_load
        :return: new content of logs.txt file
        """
        new_file_content = []  # list that will contain logs
        round_counter = 0  # counting in which round "this event" happen
        draw_counter = 0  # count how many draws was
        win_Circle = 0  # count how many wins has PlayerCircle
        win_Cross = 0  # count how many wins has PlayerCross
        for result in self.player_win_logs:
            round_counter += 1  # If there is new result, why I shouldn't call it as another round?
            if result == "d":  # when there was draw
                new_file_content.append('Round "{}" was tie.\n'.format(round_counter))  # Pytanie Wolisz format czy f ?
                draw_counter += 1
            elif result == self.player_circle.char:  # when Circle won
                new_file_content.append('Round "{}" was won by {}\n'.format(round_counter, self.player_circle.name))
                win_Circle += 1
            elif result == self.player_cross.char:  # when Cross won
                win_Cross += 1
                new_file_content.append('Round "{}" was won by {} \n'.format(round_counter, self.player_cross.name))

        # After all result saved it's time to count all informations and save them too
        new_file_content.append("In this log sesion {} won {} times, {} won {} times, and they get {} draws.\n"
                                .format(self.player_circle.name, win_Circle,
                                        self.player_cross.name, win_Cross, draw_counter))
        return new_file_content  # return list

    def logs_without_load(self):
        """
        Saving a logs from plays when player start new logs
        what mean: won't continue logging session
        :return: none
        """
        logs = self.logs()
        try:  # as 'w' not need existing file, I gave "try" just for show
            file = open('./logs.txt', 'w', encoding='utf-8')
            for each in logs:
                file.write(each)  # save each of logs list element.
            file.close()
        finally:
            pass
