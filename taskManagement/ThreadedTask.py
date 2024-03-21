import threading

from ..GenAI import AssistantConnector, Sculptor
class ThreadedTask(threading.Thread):

    def __int__(self):
        pass

    def run(self):
        process_generator = AssistantConnector(api_key, process_gen_id)
        process = process_generator.generate_completion(text)

        graphic_generator = AssistantConnector(api_key, graphic_gen_id)
        graphic = graphic_generator.generate_completion(process)

        graphic_checker = AssistantConnector(api_key, graphic_gen_id)
        checked_graphic = graphic_checker.generate_completion(graphic)

        sculptor = Sculptor()
        sculptor.sculpt(process, checked_graphic)