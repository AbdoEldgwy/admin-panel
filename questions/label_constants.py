# Question Type Labels
QUESTION_TYPES = [
    # Programming Languages
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('java', 'Java'),
    ('cpp', 'C++'),
    ('csharp', 'C#'),
    
    # Web Development
    ('html', 'HTML'),
    ('css', 'CSS'),
    ('react', 'React'),
    ('angular', 'Angular'),
    ('vue', 'Vue.js'),
    
    # Backend Frameworks
    ('django', 'Django'),
    ('flask', 'Flask'),
    ('spring', 'Spring'),
    ('express', 'Express.js'),
    ('laravel', 'Laravel'),
    
    # Database
    ('sql', 'SQL'),
    ('mongodb', 'MongoDB'),
    ('postgresql', 'PostgreSQL'),
    ('mysql', 'MySQL'),
    ('redis', 'Redis'),
    
    # DevOps
    ('docker', 'Docker'),
    ('kubernetes', 'Kubernetes'),
    ('aws', 'AWS'),
    ('azure', 'Azure'),
    ('git', 'Git'),
    
    # Computer Science Fundamentals
    ('algorithms', 'Algorithms'),
    ('data_structures', 'Data Structures'),
    ('design_patterns', 'Design Patterns'),
    ('oop', 'Object-Oriented Programming'),
    ('system_design', 'System Design'),
]

# Evaluation Points
EVALUATION_POINTS = [
    # Technical Skills
    ('problem_solving', 'Problem Solving'),
    ('code_quality', 'Code Quality'),
    ('algorithm_efficiency', 'Algorithm Efficiency'),
    ('debugging', 'Debugging Skills'),
    ('testing', 'Testing Knowledge'),
    
    # Communication
    ('technical_communication', 'Technical Communication'),
    ('documentation', 'Documentation'),
    ('code_review', 'Code Review'),
    ('team_collaboration', 'Team Collaboration'),
    ('knowledge_sharing', 'Knowledge Sharing'),
    
    # Best Practices
    ('clean_code', 'Clean Code'),
    ('security_awareness', 'Security Awareness'),
    ('performance_optimization', 'Performance Optimization'),
    ('scalability', 'Scalability'),
    ('maintainability', 'Maintainability'),
    
    # Soft Skills
    ('time_management', 'Time Management'),
    ('adaptability', 'Adaptability'),
    ('learning_ability', 'Learning Ability'),
    ('attention_to_detail', 'Attention to Detail'),
    ('critical_thinking', 'Critical Thinking'),
]

# Combine all labels
ALL_LABELS = QUESTION_TYPES + EVALUATION_POINTS

# Label Categories
LABEL_CATEGORIES = {
    'question_types': QUESTION_TYPES,
    'evaluation_points': EVALUATION_POINTS,
} 