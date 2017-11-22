import json

def line_to_dict(line):
    line_spl = line.split('|')
    line_dict = {
        'name': line_spl[0],
        'aliases': [],
        'content': line_spl[1].replace('$', '\n'),
        'color': line_spl[2],
        'aka': line_spl[3],
        'skill': line_spl[4].replace('\n', '')
    }
    return line_dict


with open('../skills.txt') as f:
    skills = f.readlines()  
    skills_dict = {}

    for skill in skills:
        skill_dict = line_to_dict(skill)
        name = skill_dict['name']
        content = skill_dict['content']

        found = False
        for s in skills_dict.values():
            if content == s['content']:
                skills_dict[s['name']]['aliases'].append(skill_dict['name'])
                found = True

        if not found:
            skills_dict[name] = skill_dict

    skills_list = list(skills_dict.values())
    with open('../skills.json', 'w') as out:
        json.dump(skills_list, out, indent=4)



  

    

    


