import yaml
import os


def get_events(processor):
    p8_file = os.path.abspath("../events/power8.yaml")
    p7_file = os.path.abspath("../events/power7.yaml")
    events_list = []
    if processor == "POWER8":
        with open(p8_file, "r") as f:
            groups = yaml.load(f)
            for i in groups.values():
                events_list.append(i)
            return events_list
    else:
        with open(p7_file, "r") as f:
            groups = yaml.load(f)
            for i in groups.values():
                events_list.append(i)
            return events_list
