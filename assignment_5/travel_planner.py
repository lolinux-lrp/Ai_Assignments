import random

# --- Mock Knowledge Bases ---

WINE_KB = {
    "red": ["Cabernet Sauvignon", "Merlot", "Pinot Noir", "Chianti"],
    "white": ["Chardonnay", "Sauvignon Blanc", "Riesling", "Pinot Grigio"],
    "sparkling": ["Champagne", "Prosecco", "Cava"]
}

PLACES_KB = {
    "adventure": ["Patagonia", "Queenstown", "Swiss Alps"],
    "culture": ["Rome", "Kyoto", "Istanbul", "Paris"],
    "relaxation": ["Maldives", "Bali", "Bora Bora"]
}

FOOD_KB = {
    "Italy": ["Pasta Carbonara", "Neapolitan Pizza", "Gelato"],
    "Japan": ["Sushi", "Ramen", "Tempura"],
    "France": ["Baguette", "Camembert Cheese", "Croissant", "Coq au Vin"],
    "Indonesia": ["Nasi Goreng", "Satay", "Gado-Gado"]
}

# Mapping places to their respective countries to look up food
PLACE_TO_COUNTRY = {
    "Rome": "Italy",
    "Kyoto": "Japan",
    "Paris": "France",
    "Bali": "Indonesia"
}

COST_ESTIMATES = {
    "Patagonia": 3000, "Queenstown": 2500, "Swiss Alps": 4000,
    "Rome": 2000, "Kyoto": 2800, "Istanbul": 1500, "Paris": 2200,
    "Maldives": 5000, "Bali": 1800, "Bora Bora": 6000
}

# --- System Components ---

class UserProfile:
    """Represents a user's preferences and constraints."""
    def __init__(self, name, interests, budget, wine_preference=None):
        self.name = name
        self.interests = interests # e.g., ['adventure', 'culture']
        self.budget = budget
        self.wine_preference = wine_preference # 'red', 'white', 'sparkling'

class AITravelPlanner:
    """AI planner that utilizes knowledge bases to generate personalized tour plans."""
    def __init__(self):
        self.places_kb = PLACES_KB
        self.wine_kb = WINE_KB
        self.food_kb = FOOD_KB
        self.cost_kb = COST_ESTIMATES
        self.place_to_country = PLACE_TO_COUNTRY

    def recommend_destinations(self, profile):
        """Filter destinations based on interests and budget."""
        recommended = []
        for interest in profile.interests:
            if interest in self.places_kb:
                recommended.extend(self.places_kb[interest])
        
        # Remove duplicates
        recommended = list(set(recommended))
        
        # Filter by budget
        affordable = [place for place in recommended if self.cost_kb.get(place, 99999) <= profile.budget]
        return affordable

    def generate_tour_plan(self, profile):
        """Generates a complete personalized tour plan string."""
        destinations = self.recommend_destinations(profile)
        
        if not destinations:
            return f"Sorry {profile.name}, we couldn't find a destination matching your interests within your budget of ${profile.budget}."
            
        selected_dest = random.choice(destinations)
        cost = self.cost_kb[selected_dest]
        
        # Infer food recommendations
        country = self.place_to_country.get(selected_dest)
        if country and country in self.food_kb:
            foods = self.food_kb[country]
        else:
            foods = ["Local street food", "Fresh regional produce"]
            
        # Infer wine recommendations
        wine = None
        if profile.wine_preference and profile.wine_preference in self.wine_kb:
            wine = random.choice(self.wine_kb[profile.wine_preference])
            
        # Construct output
        plan = []
        plan.append(f"=== Personalised Tour Plan for {profile.name} ===")
        plan.append(f"Destination: {selected_dest}")
        plan.append(f"Theme: {', '.join(profile.interests).title()}")
        plan.append(f"Estimated Cost: ${cost} (Under Budget of ${profile.budget})")
        plan.append(f"Food Recommendations: {', '.join(foods)}")
        if wine:
            plan.append(f"Wine Pairing: {wine} (Preference: {profile.wine_preference})")
        plan.append("=============================================")
        
        return "\n".join(plan)

# --- Testing ---

def test_planner():
    planner = AITravelPlanner()
    
    print("Test 1: Alice (Culture, Red Wine, Moderate Budget)")
    user1 = UserProfile(name="Alice", interests=["culture"], budget=2500, wine_preference="red")
    print(planner.generate_tour_plan(user1))
    print("\n" + "-"*50 + "\n")
    
    print("Test 2: Bob (Relaxation and Adventure, Sparkling Wine, High Budget)")
    user2 = UserProfile(name="Bob", interests=["relaxation", "adventure"], budget=6000, wine_preference="sparkling")
    print(planner.generate_tour_plan(user2))
    print("\n" + "-"*50 + "\n")
    
    print("Test 3: Charlie (Adventure, Low Budget - Expects Failure)")
    user3 = UserProfile(name="Charlie", interests=["adventure"], budget=1000)
    print(planner.generate_tour_plan(user3))

if __name__ == "__main__":
    test_planner()
