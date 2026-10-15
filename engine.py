from typing import Dict, List

PIS = {
 'CAC': {
  'SO1': ['Identify and clearly define the requirements and constraints of a complex computing problem.','Analyze the problem using appropriate computing concepts, principles, algorithms, and techniques.','Apply relevant computing and disciplinary knowledge to formulate feasible solutions.','Compare and justify alternative solutions based on appropriate technical criteria.'],
  'SO2': ['Translate computing requirements into an appropriate solution design.','Select appropriate algorithms, technologies, tools, and techniques for implementation.','Implement the proposed computing-based solution correctly.','Test and evaluate the solution against specified requirements.','Refine the solution based on testing and evaluation results.'],
  'SO3': ['Present technical information clearly and logically in written form.','Communicate technical concepts effectively through oral presentations.','Adapt communication to the intended professional audience.','Use appropriate technical terminology, documentation, diagrams, and visual aids.'],
  'SO4': ['Identify ethical, legal, privacy, security, and professional issues associated with computing practice.','Recognize the potential impact of computing solutions on individuals, organizations, and society.','Apply relevant professional codes, legal requirements, and ethical principles when making decisions.','Justify professional decisions considering ethical and societal implications.'],
  'SO5': ['Collaborate effectively with team members to accomplish assigned tasks.','Contribute effectively to team planning, coordination, and problem solving.','Demonstrate appropriate leadership when assigned responsibility.','Manage tasks, responsibilities, and timelines to achieve team objectives.','Demonstrate professional and inclusive behavior within a team.'],
  'SO6': ['Apply fundamental computer science theories and concepts to computing problems.','Apply appropriate algorithms, data structures, programming, and computational techniques.','Apply software development principles and practices in solution development.','Use appropriate software development tools and technologies.','Integrate computer science concepts to develop functional computing-based solutions.']},
 'EAC': {
  'SO1': ['Identify and define complex engineering problems.','Formulate engineering problems using appropriate mathematical and scientific principles.','Apply appropriate engineering knowledge and techniques to solve problems.','Analyze and evaluate engineering solutions.','Validate the solution using appropriate engineering criteria.'],
  'SO2': ['Identify engineering design requirements and constraints.','Develop appropriate engineering design alternatives.','Select and implement an appropriate design solution.','Consider health, safety, and welfare in engineering design.','Consider environmental, economic, social, cultural, and global factors in design.','Evaluate the effectiveness of the final design against specified needs.'],
  'SO3': ['Prepare clear and technically appropriate written communication.','Deliver effective oral presentations.','Use appropriate graphical and visual communication techniques.','Adapt communication appropriately for different audiences.'],
  'SO4': ['Identify ethical and professional issues in engineering practice.','Apply relevant professional codes and ethical principles.','Evaluate the societal, environmental, economic, and global impacts of engineering solutions.','Make and justify informed professional judgments considering relevant constraints.'],
  'SO5': ['Work effectively as a member of a diverse team.','Establish and contribute to team goals.','Plan and organize team tasks effectively.','Demonstrate leadership when appropriate.','Create and maintain a collaborative and inclusive team environment.','Complete assigned responsibilities and contribute to achieving team objectives.'],
  'SO6': ['Formulate an appropriate experimental approach.','Conduct experiments using appropriate methods, tools, and procedures.','Collect and organize experimental data accurately.','Analyze and interpret experimental results using appropriate techniques.','Apply engineering judgment to draw valid conclusions.','Identify limitations, uncertainty, or sources of error in experimental results.'],
  'SO7': ['Identify knowledge gaps or new knowledge required to address a problem.','Identify and use appropriate learning resources and strategies.','Acquire and understand new technical knowledge independently.','Apply newly acquired knowledge to solve engineering problems.','Demonstrate the ability to adapt to emerging technologies and changing professional requirements.']}
}

ASSESSMENTS = ['Internal Assessment I','Internal Assessment II','Assignment','Model Examination','Semester End Examination','Seminar','MCQs','Practical Exercises','Assessed Group Activity']

def score(covered: int, total: int) -> int:
    percentage = covered / total * 100 if total else 0
    return 3 if percentage >= 60 - 1e-9 else 2 if percentage >= 50 - 1e-9 else 0

def calculate(framework: str, cos: List[dict], selections: Dict[str, dict]) -> dict:
    if framework not in PIS: raise ValueError('Unknown framework')
    rows = []
    for co in cos:
        co_id = co['id']
        entries = {}
        for so, descriptions in PIS[framework].items():
            key = f'{co_id}|{so}'
            entry = selections.get(key, {})
            chosen = sorted(set(entry.get('pis', [])))
            allowed = {f'{so}.{i}' for i in range(1, len(descriptions)+1)}
            if not set(chosen) <= allowed:
                raise ValueError(f'Invalid PI identifiers for {key}')
            coverage = round(len(chosen) / len(descriptions) * 100, 2)
            entries[so] = {'pis':chosen,'coverage':coverage,'correlation':score(len(chosen),len(descriptions)), 'basis':entry.get('basis',''), 'rationale':entry.get('rationale',''), 'assessments':entry.get('assessments',[])}
        rows.append({'co':co_id,'description':co.get('description',''),'outcomes':entries})
    averages = {}
    for so in PIS[framework]:
        values = [r['outcomes'][so]['correlation'] for r in rows if r['outcomes'][so]['correlation'] > 0]
        averages[so] = round(sum(values)/len(values),2) if values else None
    return {'framework':framework,'rows':rows,'averages':averages}
