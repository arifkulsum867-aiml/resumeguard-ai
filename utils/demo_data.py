SAMPLE_RESUMES = {
    "Sample Resume 1": """
JOHN DOE
Email: john.doe@email.com | Phone: (555) 123-4567 | LinkedIn: linkedin.com/in/johndoe

SUMMARY
Results-driven Data Scientist with 3+ years of experience in machine learning and data analysis. 
Proven track record of developing predictive models and deriving actionable insights from complex datasets.

EDUCATION
Master of Science in Data Science
University of California, Berkeley | May 2021
GPA: 3.8/4.0

Bachelor of Science in Computer Science
University of Texas, Austin | May 2019
GPA: 3.9/4.0

EXPERIENCE
Senior Data Scientist
Tech Company, San Francisco | June 2022 - Present
• Developed machine learning model that increased accuracy by 23% on customer churn prediction
• Led team of 3 junior data scientists on NLP project, reducing processing time by 40%
• Implemented automated data pipeline using Python and Airflow, saving 15 hours/week of manual work
• Presented quarterly insights to executive team, influencing $2M in strategic decisions

Data Scientist
Analytics Firm, Austin | July 2021 - May 2022
• Built predictive models using scikit-learn and TensorFlow achieving 92% accuracy
• Conducted exploratory data analysis on datasets with 10M+ records
• Created interactive dashboards using Tableau and Plotly for stakeholders
• Mentored 2 interns on Python best practices and machine learning fundamentals

SKILLS
Technical Skills: Python, SQL, Scala, Java, R, JavaScript, TypeScript
Data Analysis: Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, Keras
Visualization: Tableau, Power BI, Plotly, Matplotlib, Seaborn
Databases: PostgreSQL, MongoDB, Cassandra, Redis
Cloud: AWS (EC2, S3, SageMaker), Google Cloud Platform, Azure
Tools: Jupyter, Git, Docker, Kubernetes, Jenkins, Apache Spark

PROJECTS
Customer Segmentation ML Model (2022)
• Developed K-means clustering algorithm to segment 500K customers into 5 distinct groups
• Improved marketing ROI by 35% through targeted campaigns based on segments
• Tech stack: Python, Scikit-learn, PostgreSQL, Flask

Time Series Forecasting Application (2021)
• Built LSTM neural network to predict stock prices with 87% accuracy
• Deployed model using Docker on AWS EC2
• Tech stack: Python, TensorFlow, AWS, Docker

CERTIFICATIONS
AWS Certified Machine Learning - Specialty | Amazon | 2022
TensorFlow Developer Certificate | Google | 2021
""",
    "Sample Resume 2": """
JANE SMITH
Email: jane.smith@email.com | LinkedIn: linkedin.com/in/janesmith | GitHub: github.com/janesmith

PROFESSIONAL SUMMARY
Full-stack software engineer with 5+ years of experience building scalable web applications. 
Expertise in React, Node.js, and cloud technologies. Passionate about clean code and user experience.

EDUCATION
Bachelor of Science in Information Technology
State University | May 2018

WORK EXPERIENCE
Senior Full-Stack Developer
Web Solutions Inc., New York | March 2021 - Present
• Architected microservices platform using Node.js that handles 1M+ requests daily
• Led frontend migration from AngularJS to React, reducing load time by 45%
• Established code review practices and CI/CD pipelines using Jenkins
• Mentored team of 5 junior developers

Full-Stack Developer
Digital Agency, Boston | August 2019 - February 2021
• Developed 15+ responsive web applications using React and Vue.js
• Optimized database queries improving application performance by 60%
• Implemented AWS infrastructure including EC2, RDS, and S3
• Collaborated with UX team to deliver pixel-perfect implementations

Junior Developer
StartUp Company, Boston | June 2018 - July 2019
• Built RESTful APIs using Express.js and Flask
• Developed responsive UI components with HTML5, CSS3, JavaScript
• Assisted in database design and optimization

TECHNICAL SKILLS
Languages: JavaScript, TypeScript, Python, Java, SQL
Frontend: React, Vue.js, Angular, HTML5, CSS3, Bootstrap, Material-UI, Tailwind CSS
Backend: Node.js, Express.js, Flask, Django, RESTful APIs, GraphQL
Databases: PostgreSQL, MongoDB, MySQL, Redis
Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Jenkins, GitHub Actions
Tools: Git, VSCode, Postman, Jira, Figma

PROJECTS
E-commerce Platform (2022)
• Built full-stack application with React frontend and Node.js backend
• Implemented payment processing with Stripe
• Deployed on AWS using Docker and Kubernetes
• Results: Processed $500K in transactions

Task Management App (2021)
• Created collaborative task application using React and Firebase
• Real-time updates using WebSockets
• 1000+ active users

CERTIFICATIONS
AWS Certified Solutions Architect - Associate | 2021
"""
}

SAMPLE_JOB_DESCRIPTIONS = {
    "Data Scientist Position": """
Position: Senior Data Scientist
Company: Tech Innovations Corp
Location: Remote

Job Description:
We are looking for an experienced Data Scientist to join our growing Analytics team. 
You will be responsible for developing machine learning models and driving data-driven decisions.

Key Responsibilities:
• Develop and deploy machine learning models for predictive analytics
• Analyze large datasets to identify trends and insights
• Collaborate with engineering teams to implement solutions
• Mentor junior data scientists and interns
• Present findings to business stakeholders

Required Skills:
• 3+ years of experience in data science or machine learning
• Proficiency in Python, R, or Scala
• Experience with ML libraries (scikit-learn, TensorFlow, PyTorch)
• Strong SQL and database knowledge
• Experience with cloud platforms (AWS, GCP, Azure)
• Excellent communication skills
• Knowledge of statistics and probability

Nice to Have:
• Experience with NLP or computer vision
• Published research or Kaggle competitions
• Experience with Apache Spark or big data technologies
• AWS or Google Cloud certifications

Education:
• Master's degree in Computer Science, Statistics, or related field
• or equivalent professional experience

Compensation: $150K - $200K + benefits
""",
    "Full-Stack Developer Position": """
Position: Senior Full-Stack Developer
Company: Digital Innovations Ltd
Location: Hybrid (New York)

Job Description:
Join our engineering team to build scalable, high-performance web applications. 
We need someone who can own features end-to-end, from database design to user interface.

Responsibilities:
• Design and develop scalable backend services and APIs
• Build responsive and intuitive user interfaces
• Optimize application performance and security
• Participate in code reviews and technical discussions
• Collaborate with product and design teams
• Deploy applications to production environments
• Troubleshoot and debug production issues

Required Qualifications:
• 5+ years of full-stack development experience
• Strong proficiency in JavaScript/TypeScript
• Experience with React or Vue.js
• Backend development with Node.js, Django, or similar
• Database design and optimization (SQL/NoSQL)
• Git and version control
• Understanding of REST APIs and microservices
• Strong problem-solving skills

Preferred Qualifications:
• Experience with Docker and Kubernetes
• Cloud deployment (AWS, GCP, Azure)
• CI/CD pipeline implementation
• Experience with GraphQL
• Performance optimization experience
• Leadership or mentoring experience

Education:
• Bachelor's degree in Computer Science or related field
• or equivalent industry experience

Salary: $130K - $170K + benefits + stock options
Benefits: Health insurance, 401k, unlimited PTO, professional development
"""
}

def get_sample_resume(name):
    """Get a sample resume by name."""
    return SAMPLE_RESUMES.get(name, "")

def get_sample_job_description(name):
    """Get a sample job description by name."""
    return SAMPLE_JOB_DESCRIPTIONS.get(name, "")

def list_sample_resumes():
    """List all available sample resumes."""
    return list(SAMPLE_RESUMES.keys())

def list_sample_jobs():
    """List all available sample job descriptions."""
    return list(SAMPLE_JOB_DESCRIPTIONS.keys())
