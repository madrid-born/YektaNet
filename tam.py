class Skill:
    def __init__(self, name):
        self.name = name
        self.view = 0

    def __init__(self, name, view):
        self.name = name
        self.view = view

def showList(skill_list):
    # Custom sorting key to sort by 'view' and then by 'name'
    def sorting_key(skill):
        return (-skill.view, skill.name)

    # Sorting the list using the custom key
    sorted_list = sorted(skill_list, key=sorting_key)

    return sorted_list

# Example usage:
skills = [Skill("B", 0), Skill("A", 2), Skill("C", 3), Skill("C", view=1), Skill("B", view=1)]
sorted_skills = showList(skills)
for skill in sorted_skills:
    print(f"Name: {skill.name}, View: {skill.view}")
