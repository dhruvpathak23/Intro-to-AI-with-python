import random
import os
from PIL import Image, ImageDraw


class Space():

    def __init__(self, height, width, num_hospitals):
        """Create the grid with given size and number of hospitals."""
        self.height = height
        self.width = width
        self.num_hospitals = num_hospitals
        self.houses = set()
        self.hospitals = set()

    def add_house(self, row, col):
        """Add a house at a specific row and column."""
        self.houses.add((row, col))

    def available_spaces(self):
        """Return all empty cells (not house, not hospital)."""
        candidates = set(
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
        )
        return candidates - self.houses - self.hospitals

    def get_cost(self, hospitals):
        """Calculate total Manhattan distance from each house to nearest hospital."""
        cost = 0
        for house in self.houses:
            distance = min(
                abs(house[0] - hospital[0]) + abs(house[1] - hospital[1])
                for hospital in hospitals
            )
            cost += distance
        return cost

    def get_neighbors(self):
        """Generate all possible neighbor states by moving one hospital."""
        neighbors = []
        for hospital in self.hospitals:
            for space in self.available_spaces():
                new_state = self.hospitals.copy()
                new_state.remove(hospital)
                new_state.add(space)
                neighbors.append(new_state)
        return neighbors

    def hill_climb(self, maximum=None, image_prefix=None, log=False):
        """Run hill climbing search to minimize cost."""
        count = 0

        # Initialize hospitals randomly
        self.hospitals = set(
            random.sample(
                list({
                    (r, c)
                    for r in range(self.height)
                    for c in range(self.width)
                } - self.houses),
                self.num_hospitals
            )
        )

        if log:
            print(f"Initial cost: {self.get_cost(self.hospitals)}")

        if image_prefix:
            self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")

        while maximum is None or count < maximum:
            count += 1
            current_cost = self.get_cost(self.hospitals)
            neighbors = self.get_neighbors()

            if not neighbors:
                break

            best_cost = None
            best_neighbors = []

            for neighbor in neighbors:
                cost = self.get_cost(neighbor)
                if best_cost is None or cost < best_cost:
                    best_cost = cost
                    best_neighbors = [neighbor]
                elif cost == best_cost:
                    best_neighbors.append(neighbor)

            if best_cost >= current_cost:
                return self.hospitals

            self.hospitals = random.choice(best_neighbors)

            if log:
                print(f"Step {count}: cost {best_cost}")

            if image_prefix:
                self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")

        return self.hospitals

    def random_restart(self, restarts, image_prefix=None, log=False):
        """Run hill climbing multiple times and keep the best result."""
        best_solution = None
        best_cost = None

        for i in range(restarts):
            if log:
                print(f"--- Restart {i + 1} ---")
            
            # Run hill climb (state is reset inside hill_climb)
            solution = self.hill_climb(
                image_prefix=f"{image_prefix}_r{i}_" if image_prefix else None,
                log=log
            )
            cost = self.get_cost(solution)

            if best_cost is None or cost < best_cost:
                best_cost = cost
                best_solution = solution

        self.hospitals = best_solution
        return best_solution

    def output_image(self, filename):
        """Generate an image of the current state."""
        cell_size = 50
        cell_border = 2
        padding = 20

        img_width = self.width * cell_size + padding * 2
        img_height = self.height * cell_size + padding * 2 + 40

        # Create RGBA background to support transparency
        img = Image.new("RGBA", (img_width, img_height), "black")
        draw = ImageDraw.Draw(img)

        # Determine the base directory for images
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Load and convert icons to RGBA
        house_path = os.path.join(base_dir, "house.png")
        hospital_path = os.path.join(base_dir, "hospital.png")
        
        # FIX: Added .convert("RGBA") to handle transparency mask correctly
        house = Image.open(house_path).convert("RGBA").resize((cell_size - 10, cell_size - 10))
        hospital = Image.open(hospital_path).convert("RGBA").resize((cell_size - 10, cell_size - 10))

        for row in range(self.height):
            for col in range(self.width):
                x1 = padding + col * cell_size
                y1 = padding + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                draw.rectangle(
                    [x1, y1, x2, y2],
                    outline="white",
                    width=cell_border
                )

                if (row, col) in self.houses:
                    img.paste(house, (x1 + 5, y1 + 5), house)

                if (row, col) in self.hospitals:
                    img.paste(hospital, (x1 + 5, y1 + 5), hospital)

        # Draw cost text
        cost = self.get_cost(self.hospitals)
        draw.text(
            (padding, img_height - 30),
            f"Cost: {cost}",
            fill="white"
        )

        img.save(filename)


# -------- Driver Code --------

if __name__ == "__main__":

    # Create space
    s = Space(height=10, width=20, num_hospitals=3)

    # Add 15 random houses
    for i in range(15):
        s.add_house(
            random.randrange(s.height),
            random.randrange(s.width)
        )

    # Run random restart hill climbing
    # This will try 5 times and keep the best result
    hospitals = s.random_restart(restarts=5, image_prefix="hospitals", log=True)

    print("\nFinal hospital locations:", hospitals)
    print("Final cost:", s.get_cost(hospitals))