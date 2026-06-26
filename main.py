import time

class MealPrepAgent:
    def __init__(self, goal="Prepare a simple salad"):
        self.goal = goal
        self.required_ingredients = ["lettuce", "tomato", "cucumber", "dressing"]
        self.inventory = set()
        self.chopped_ingredients = set()
        self.salad_mixed = False
        self.meal_served = False
        print(f"Agent initialized with goal: '{self.goal}'")
        print(f"Required ingredients: {', '.join(self.required_ingredients)}\n")

    # --- Simulated Tools/Actions ---
    def _get_ingredient(self, item):
        if item not in self.inventory:
            print(f"ACTION: Getting '{item}'...")
            time.sleep(0.1) # Simulate work
            self.inventory.add(item)
            print(f"  Acquired '{item}'. Inventory: {', '.join(self.inventory)}")
            return True
        return False

    def _chop_ingredient(self, item):
        if item in self.inventory and item not in self.chopped_ingredients:
            print(f"ACTION: Chopping '{item}'...")
            time.sleep(0.1) # Simulate work
            self.chopped_ingredients.add(item)
            print(f"  Chopped '{item}'. Chopped: {', '.join(self.chopped_ingredients)}")
            return True
        return False

    def _mix_salad(self):
        # Can only mix if all non-dressing ingredients are chopped
        ingredients_to_chop = [ing for ing in self.required_ingredients if ing != "dressing"]
        if not self.salad_mixed and all(ing in self.chopped_ingredients for ing in ingredients_to_chop):
            print("ACTION: Mixing the salad...")
            time.sleep(0.1)
            self.salad_mixed = True
            print("  Salad is mixed!")
            return True
        return False

    def _serve_meal(self):
        if self.salad_mixed and not self.meal_served:
            print("ACTION: Serving the meal...")
            time.sleep(0.1)
            self.meal_served = True
            print("  Meal served! Goal achieved.")
            return True
        return False

    # --- Goal Check ---
    def _is_goal_achieved(self):
        return self.meal_served

    # --- Decision Logic (Core of Agentic AI) ---
    def _decide_next_action(self, strategy_mode="tactical"):
        if self._is_goal_achieved():
            return False # No more actions needed

        if strategy_mode == "tactical":
            # TACTICAL: React to the immediate next step needed.
            # Prioritize getting missing ingredients, then chopping, then mixing, then serving.
            print("DECISION (Tactical): Evaluating immediate needs...")
            for ingredient in self.required_ingredients:
                if ingredient not in self.inventory:
                    # Tactical: Get the first missing ingredient found
                    if self._get_ingredient(ingredient):
                        return True
            
            for ingredient in self.inventory:
                # Exclude dressing from chopping, as it's typically added directly.
                if ingredient not in self.chopped_ingredients and ingredient != "dressing":
                    # Tactical: Chop the first acquired, unchopped ingredient
                    if self._chop_ingredient(ingredient):
                        return True
            
            # Check if all chop-able ingredients are chopped before mixing
            ingredients_to_chop = [ing for ing in self.required_ingredients if ing != "dressing"]
            if not self.salad_mixed and all(ing in self.chopped_ingredients for ing in ingredients_to_chop):
                # Tactical: Mix if possible
                if self._mix_salad():
                    return True
            
            if self.salad_mixed and not self.meal_served:
                # Tactical: Serve if possible
                if self._serve_meal():
                    return True

        elif strategy_mode == "strategic":
            # STRATEGIC: Follow a phased plan, ensuring comprehensive prerequisites before moving to next phase.
            print("DECISION (Strategic): Following a phased plan...")
            
            # Phase 1: Acquire all ingredients
            missing_ingredients = [ing for ing in self.required_ingredients if ing not in self.inventory]
            if missing_ingredients:
                print(f"  Strategic Phase 1: Acquiring all ingredients. Missing: {', '.join(missing_ingredients)}")
                # Strategic: Prioritize getting ANY missing ingredient to complete this phase
                if self._get_ingredient(missing_ingredients[0]): 
                    return True
            
            # Phase 2: Chop all acquired ingredients (excluding dressing)
            ingredients_to_chop = [ing for ing in self.required_ingredients if ing != "dressing"]
            unchopped_acquired = [ing for ing in self.inventory if ing in ingredients_to_chop and ing not in self.chopped_ingredients]
            
            if not missing_ingredients and unchopped_acquired:
                print(f"  Strategic Phase 2: Chopping all acquired ingredients. Unchopped: {', '.join(unchopped_acquired)}")
                # Strategic: Prioritize chopping ANY unchopped ingredient to complete this phase
                if self._chop_ingredient(unchopped_acquired[0]): 
                    return True

            # Phase 3: Mix the salad
            if not missing_ingredients and not unchopped_acquired and not self.salad_mixed:
                print("  Strategic Phase 3: Mixing the salad.")
                if self._mix_salad():
                    return True
            
            # Phase 4: Serve the meal
            if self.salad_mixed and not self.meal_served:
                print("  Strategic Phase 4: Serving the meal.")
                if self._serve_meal():
                    return True
        
        return False # No action taken this turn, or goal achieved

    def run(self, strategy_mode="tactical"):
        print(f"--- Running Agent in '{strategy_mode.upper()}' Mode ---")
        steps = 0
        while not self._is_goal_achieved() and steps < 20: # Max steps to prevent infinite loop
            print(f"\n--- Step {steps + 1} ---")
            action_taken = self._decide_next_action(strategy_mode)
            if not action_taken and not self._is_goal_achieved():
                print("No further actions can be taken towards the goal in this step.")
                break
            steps += 1
        
        if self._is_goal_achieved():
            print(f"\nGoal '{self.goal}' achieved in {steps} steps using {strategy_mode} strategy!")
        else:
            print(f"\nAgent stopped after {steps} steps. Goal not fully achieved.")

if __name__ == "__main__":
    # Example 1: Tactical Approach
    print("--- DEMONSTRATION 1: TACTICAL APPROACH ---")
    tactical_agent = MealPrepAgent()
    tactical_agent.run(strategy_mode="tactical")
    print("\n" + "="*50 + "\n")

    # Example 2: Strategic Approach
    print("--- DEMONSTRATION 2: STRATEGIC APPROACH ---")
    strategic_agent = MealPrepAgent() # Reset agent for a clean run
    strategic_agent.run(strategy_mode="strategic")