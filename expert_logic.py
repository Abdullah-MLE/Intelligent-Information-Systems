import collections.abc
# Patch for Python 3.10+ compatibility with experta/frozendict
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping

from experta import *

class UserChoice(Fact):
    """Fact representing a user's choice for a specific attribute."""
    pass

class Question(Fact):
    """Fact representing the current question to ask the user."""
    pass

class Recommendation(Fact):
    """Fact representing the final career recommendation."""
    pass

class CareerEngine(KnowledgeEngine):
    
    # --------------------------------------------------------------------------
    # Initial State
    # --------------------------------------------------------------------------
    @DefFacts()
    def _initial_action(self):
        yield Question(id='field_interest', 
                       text="What area of technology interests you the most?",
                       options=['Software Development', 'Data & AI', 'Systems & Infrastructure', 'Design & Creative', 'Management & Strategy'])

    # --------------------------------------------------------------------------
    # Level 1: Broad Interest
    # --------------------------------------------------------------------------
    @Rule(UserChoice(question='field_interest', answer='Software Development'))
    def ask_dev_platform(self):
        self.declare(Question(id='dev_platform', 
                              text="Which platform do you want to build for?", 
                              options=['Web', 'Mobile', 'Desktop', 'Game Development', 'Embedded Systems']))

    @Rule(UserChoice(question='field_interest', answer='Data & AI'))
    def ask_data_ai_focus(self):
        self.declare(Question(id='data_ai_focus', 
                              text="Do you prefer analyzing data, building models, or working with logic?", 
                              options=['Artificial Intelligence (AI)', 'Data Science', 'Data Analysis', 'Data Engineering']))

    @Rule(UserChoice(question='field_interest', answer='Systems & Infrastructure'))
    def ask_sys_focus(self):
        self.declare(Question(id='sys_focus', 
                              text="What aspect of systems interests you?", 
                              options=['Cloud & DevOps', 'Cybersecurity', 'Database Management', 'Network Engineering']))

    @Rule(UserChoice(question='field_interest', answer='Design & Creative'))
    def ask_design_focus(self):
        self.declare(Question(id='design_focus', 
                              text="What kind of design?", 
                              options=['UI/UX Design', 'Graphis & Animation', 'Technical Writing']))
    
    @Rule(UserChoice(question='field_interest', answer='Management & Strategy'))
    def ask_mgmt_focus(self):
        self.declare(Question(id='mgmt_focus', 
                              text="What kind of management?", 
                              options=['Product Management', 'Project Management', 'Tech Sales', 'Scrum Master']))

    # --------------------------------------------------------------------------
    # Level 2: Development -> Platform
    # --------------------------------------------------------------------------
    
    # --- Web ---
    @Rule(UserChoice(question='dev_platform', answer='Web'))
    def ask_web_focus(self):
        self.declare(Question(id='web_focus', 
                              text="Which part of web development?", 
                              options=['Frontend (Visuals)', 'Backend (Server Logic)', 'Full Stack (Both)']))

    @Rule(UserChoice(question='web_focus', answer='Frontend (Visuals)'))
    def ask_web_frontend_tech(self):
        self.declare(Question(id='web_frontend_tech', 
                              text="Pick a specific ecosystem:",
                              options=['React', 'Angular', 'Vue.js', 'Svelte', 'Plain HTML/CSS/JS']))

    @Rule(UserChoice(question='web_focus', answer='Backend (Server Logic)'))
    def ask_web_backend_tech(self):
        self.declare(Question(id='web_backend_tech', 
                              text="Pick a language preference:",
                              options=['Python (Django/Flask)', 'Node.js (Express/Nest)', 'Java (Spring)', 'C# (.NET)', 'PHP (Laravel)', 'Go', 'Ruby on Rails']))

    @Rule(UserChoice(question='web_focus', answer='Full Stack (Both)'))
    def ask_web_fullstack_tech(self):
        self.declare(Question(id='web_fullstack_tech', 
                              text="Which combination?",
                              options=['MERN Stack', 'MEAN Stack', '.NET Full Stack', 'Java Full Stack']))

    # --- Mobile ---
    @Rule(UserChoice(question='dev_platform', answer='Mobile'))
    def ask_mobile_type(self):
        self.declare(Question(id='mobile_type', 
                              text="Native or Cross-Platform?", 
                              options=['Cross-Platform', 'Native Android', 'Native iOS']))

    @Rule(UserChoice(question='mobile_type', answer='Cross-Platform'))
    def ask_mobile_cross(self):
        self.declare(Question(id='mobile_cross', 
                              text="Which framework?", 
                              options=['Flutter (Dart)', 'React Native (JS)', 'Kotlin Multiplatform', 'Xamarin/MAUI']))

    # --- Desktop ---
    @Rule(UserChoice(question='dev_platform', answer='Desktop'))
    def ask_desktop(self):
        self.declare(Question(id='desktop_tech', 
                              text="Preferred language?", 
                              options=['C# (.NET/WPF)', 'C++ (Qt)', 'Electron (JS)', 'Java (Swing/FX)']))

    # --- Game ---
    @Rule(UserChoice(question='dev_platform', answer='Game Development'))
    def ask_game(self):
        self.declare(Question(id='game_engine', 
                              text="Which engine?", 
                              options=['Unity (C#)', 'Unreal Engine (C++)', 'Godot', 'Custom Engine (C++/OpenGL)']))

    # --- Embedded ---
    @Rule(UserChoice(question='dev_platform', answer='Embedded Systems'))
    def ask_embedded(self):
        self.declare(Question(id='embedded_tech', 
                              text="Focus area?", 
                              options=['Embedded C/C++', 'IoT Development', 'Firmware Engineering', 'Robotics']))

    # --------------------------------------------------------------------------
    # Level 2: Data & AI
    # --------------------------------------------------------------------------
    
    # --- AI ---
    @Rule(UserChoice(question='data_ai_focus', answer='Artificial Intelligence (AI)'))
    def ask_ai_domain(self):
        self.declare(Question(id='ai_domain', 
                              text="Which AI domain?", 
                              options=['Computer Vision', 'Natural Language Processing (NLP)', 'GenAI / LLMs', 'Reinforcement Learning', 'Robotics AI']))

    # --- Data Science/Analysis ---
    @Rule(UserChoice(question='data_ai_focus', answer='Data Science'))
    def rec_data_science(self):
        self.declare(Question(id='ds_focus', 
                            text="Focus?",
                            options=['Predictive Modeling', 'Statistical Analysis']))

    @Rule(UserChoice(question='data_ai_focus', answer='Data Analysis'))
    def rec_data_analysis(self):
        self.declare(Question(id='da_tools', text="Preferred Tool?", options=['Python (Pandas)', 'Power BI / Tableau', 'SQL Analysis']))

    @Rule(UserChoice(question='data_ai_focus', answer='Data Engineering'))
    def rec_data_eng(self):
        self.declare(Question(id='de_tools', text="Focus?", options=['Big Data (Spark/Hadoop)', 'ETL Pipelines', 'Data Warehousing']))

    # --------------------------------------------------------------------------
    # Level 2: Systems
    # --------------------------------------------------------------------------
    
    @Rule(UserChoice(question='sys_focus', answer='Cloud & DevOps'))
    def ask_cloud(self):
        self.declare(Question(id='cloud_role', 
                              text="Specific Role?", 
                              options=['DevOps Engineer', 'Cloud Architect (AWS)', 'Cloud Architect (Azure)', 'SRE (Site Reliability Engineering)']))

    @Rule(UserChoice(question='sys_focus', answer='Cybersecurity'))
    def ask_security(self):
        self.declare(Question(id='sec_role', 
                              text="Specific Role?", 
                              options=['Penetration Testing (Ethical Hacking)', 'Security Analyst', 'Cryptography Engineer', 'App Security']))

    @Rule(UserChoice(question='sys_focus', answer='Database Management'))
    def ask_dba(self):
        self.declare(Question(id='dba_role', text="Type?", options=['SQL DBA (PostgreSQL/Oracle)', 'NoSQL DBA (Mongo/Cassandra)']))
    
    @Rule(UserChoice(question='sys_focus', answer='Network Engineering'))
    def rec_net(self):
        self.declare(Recommendation(track='Network Engineer (Cisco/Juniper)', description='Design and manage network infrastructure.'))

    # --------------------------------------------------------------------------
    # Recommendation Rules (Leaf Nodes)
    # --------------------------------------------------------------------------

    # Development -> Web
    @Rule(UserChoice(question='web_frontend_tech', answer=MATCH.a))
    def rec_web_front(self, a): self.declare(Recommendation(track=f'Web Frontend Developer ({a})', description='Build interactive user interfaces for the web.'))

    @Rule(UserChoice(question='web_backend_tech', answer=MATCH.a))
    def rec_web_back(self, a): self.declare(Recommendation(track=f'Web Backend Developer ({a})', description='Build server-side logic and APIs.'))
    
    @Rule(UserChoice(question='web_fullstack_tech', answer=MATCH.a))
    def rec_web_full(self, a): self.declare(Recommendation(track=f'Full Stack Developer ({a})', description='Handle both frontend and backend development.'))

    # Development -> Mobile
    @Rule(UserChoice(question='mobile_cross', answer=MATCH.a))
    def rec_mobile_cross(self, a): self.declare(Recommendation(track=f'Mobile Developer - {a}', description='Build apps for both iOS and Android with one codebase.'))
    
    @Rule(UserChoice(question='mobile_type', answer='Native Android'))
    def rec_mobile_android(self): self.declare(Recommendation(track='Android Developer (Kotlin/Java)', description='Build high-performance native Android apps.'))
    
    @Rule(UserChoice(question='mobile_type', answer='Native iOS'))
    def rec_mobile_ios(self): self.declare(Recommendation(track='iOS Developer (Swift)', description='Build high-performance native iOS apps.'))

    # Development -> Desktop
    @Rule(UserChoice(question='desktop_tech', answer=MATCH.a))
    def rec_desktop(self, a): self.declare(Recommendation(track=f'Desktop App Developer ({a})', description='Create powerful desktop applications.'))
    
    # Development -> Game
    @Rule(UserChoice(question='game_engine', answer=MATCH.a))
    def rec_game(self, a): self.declare(Recommendation(track=f'Game Developer ({a})', description='Create 2D/3D video games.'))

    # Development -> Embedded
    @Rule(UserChoice(question='embedded_tech', answer=MATCH.a))
    def rec_embedded(self, a): self.declare(Recommendation(track=f'{a} Specialist', description='Work close to the hardware.'))

    # Data & AI -> AI
    @Rule(UserChoice(question='ai_domain', answer=MATCH.a))
    def rec_ai(self, a): self.declare(Recommendation(track=f'AI Engineer - {a}', description='Develop intelligent systems and models.'))

    # Data & AI -> Data
    @Rule(UserChoice(question='ds_focus', answer=MATCH.a))
    def rec_ds(self, a): self.declare(Recommendation(track=f'Data Scientist ({a})', description='Extract insights and build predictive models.'))

    @Rule(UserChoice(question='da_tools', answer=MATCH.a))
    def rec_da(self, a): self.declare(Recommendation(track=f'Data Analyst ({a})', description='Analyze and visualize data trends.'))

    @Rule(UserChoice(question='de_tools', answer=MATCH.a))
    def rec_de(self, a): self.declare(Recommendation(track=f'Data Engineer ({a})', description='Build scalable data pipelines.'))

    # Systems
    @Rule(UserChoice(question='cloud_role', answer=MATCH.a))
    def rec_cloud(self, a): self.declare(Recommendation(track=f'{a}', description='Manage cloud infrastructure and deployments.'))

    @Rule(UserChoice(question='sec_role', answer=MATCH.a))
    def rec_sec(self, a): self.declare(Recommendation(track=f'Cybersecurity - {a}', description='Protect systems networks and data.'))
    
    @Rule(UserChoice(question='dba_role', answer=MATCH.a))
    def rec_dba(self, a): self.declare(Recommendation(track=f'Database Administrator ({a})', description='Manage and optimize database performance.'))

    # Design
    @Rule(UserChoice(question='design_focus', answer=MATCH.a))
    def rec_design(self, a): self.declare(Recommendation(track=f'{a}', description='Design user experiences or visuals.'))

    # Mgmt
    @Rule(UserChoice(question='mgmt_focus', answer=MATCH.a))
    def rec_mgmt(self, a): self.declare(Recommendation(track=f'{a}', description='Lead teams or products to success.'))
