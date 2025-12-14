import customtkinter as ctk
from expert_logic import CareerEngine, UserChoice, Question, Recommendation, Fact

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CareerWizardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Career Path Expert System")
        self.geometry("800x600")
        
        # Expert System Engine
        self.engine = CareerEngine()
        self.engine.reset()
        
        # UI Components
        self.setup_ui()
        
        # Start the engine logic
        self.current_question_id = None
        self.process_engine_state()

    def setup_ui(self):
        # Header
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.pack(pady=20, padx=20, fill="x")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Tech Career Advisor", font=("Roboto", 24, "bold"))
        self.title_label.pack(pady=10)
        
        self.progress_label = ctk.CTkLabel(self.header_frame, text="Let's find your path...", font=("Roboto", 14))
        self.progress_label.pack(pady=5)

        # Content Area
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.question_label = ctk.CTkLabel(self.content_frame, text="", font=("Roboto", 20), wraplength=700)
        self.question_label.pack(pady=40, padx=20)
        
        self.options_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.options_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Action Area
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(pady=20, padx=20, fill="x")
        
        self.reset_button = ctk.CTkButton(self.action_frame, text="Restart", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.reset_system)
        self.reset_button.pack(side="left")

    def process_engine_state(self):
        """Runs the engine and updates the UI based on new facts."""
        self.engine.run()
        
        # Check for Recommendation first (Leaf node)
        recommendation = None
        question = None
        
        # Iterate through facts to find the latest Question or Recommendation
        # Experta stores facts in a dict-like structure. We need to find the one we haven't acted on or the most relevant one.
        # Since we are adding facts sequentially, we can look for specific types.
        
        for fact_id, fact in self.engine.facts.items():
            if isinstance(fact, Recommendation):
                recommendation = fact
                break
            if isinstance(fact, Question):
                # Check if this question has been answered already
                # We can track answered question IDs
                if fact.get('id') != self.current_question_id:
                    # Potential new question
                    # But wait, checking if we already answered this is tricky if we don't store history.
                    # Simplified approach: The engine rules trigger new questions based on answers.
                    # We just need to find the question that does NOT have a corresponding UserChoice yet?
                    # Or simpler: The engine produces ONE Question at a time if we design it right.
                    # My design produces a Question. If I answer it, the Next rule fires and creates a NEW question.
                    # So I should always pick the *latest* declared question basically.
                    question = fact

        if recommendation:
            self.show_recommendation(recommendation)
        elif question:
            # Only update if it's a new question to avoid loop/flicker
            # Ideally we check if this question ID is different from the last one we displayed
            # However, since 'run()' is idempotent until new declarations, we can just display safe.
            # But we must distinguish between "old question already answered" and "new question".
            # The 'UserChoice' fact connects to the question ID.
            
           is_answered = False
           for fid, f in self.engine.facts.items():
               if isinstance(f, UserChoice) and f.get('question') == question['id']:
                   is_answered = True
                   break
           
           if not is_answered:
               self.current_question_id = question['id']
               self.show_question(question)
           else:
               # If the only question found is one we answered, and no recommendation,
               # it means something is stuck or we are traversing. 
               # Actually, our rules chain one question to another.
               pass 

    def show_question(self, question_fact):
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
            
        self.question_label.configure(text=question_fact['text'])
        
        options = question_fact['options']
        
        for option in options:
            btn = ctk.CTkButton(self.options_frame, text=option, 
                                font=("Roboto", 16), 
                                height=40,
                                command=lambda opt=option: self.handle_answer(question_fact['id'], opt))
            btn.pack(pady=10, fill="x", padx=100)
            
    def show_recommendation(self, rec_fact):
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
            
        self.question_label.configure(text=f"Recommended Track:\n{rec_fact['track']}")
        
        desc_label = ctk.CTkLabel(self.options_frame, text=rec_fact['description'], font=("Roboto", 18), wraplength=600)
        desc_label.pack(pady=20)
        
        final_label = ctk.CTkLabel(self.options_frame, text="Good luck on your journey!", font=("Roboto", 16, "italic"))
        final_label.pack(pady=20)

    def handle_answer(self, question_id, answer):
        # Declare the user's choice
        self.engine.declare(UserChoice(question=question_id, answer=answer))
        
        # Run the engine again to proceed
        self.process_engine_state()

    def reset_system(self):
        self.engine = CareerEngine()
        self.engine.reset()
        self.current_question_id = None
        self.process_engine_state()

if __name__ == "__main__":
    app = CareerWizardApp()
    app.mainloop()
