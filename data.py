# data.py
# Hollywood actress database. Add as many as you want.
# Each entry: name, birth, nationality, notable_films, awards, bio, category

ACTRESSES = {
    "scarlett johansson": {
        "name": "Scarlett Johansson",
        "birth": "November 22, 1984",
        "nationality": "American",
        "notable_films": ["Lost in Translation", "Marriage Story", "Black Widow", "Jojo Rabbit"],
        "awards": ["Tony Award", "BAFTA Award", "Multiple Oscar nominations"],
        "bio": "One of the highest-paid actresses in the world, known for both blockbuster roles and dramatic performances.",
        "category": "A-List"
    },
    "meryl streep": {
        "name": "Meryl Streep",
        "birth": "June 22, 1949",
        "nationality": "American",
        "notable_films": ["The Devil Wears Prada", "Sophie's Choice", "Kramer vs. Kramer", "The Iron Lady"],
        "awards": ["3 Academy Awards", "8 Golden Globes", "2 BAFTA Awards"],
        "bio": "Widely regarded as one of the greatest actresses of all time, with a record 21 Oscar nominations.",
        "category": "Oscar Winners"
    },
    "emma stone": {
        "name": "Emma Stone",
        "birth": "November 6, 1988",
        "nationality": "American",
        "notable_films": ["La La Land", "Poor Things", "The Favourite", "Easy A"],
        "awards": ["2 Academy Awards", "BAFTA Award", "Golden Globe"],
        "bio": "Known for her versatility in musicals, comedy, and dramatic roles.",
        "category": "Oscar Winners"
    },
    "jennifer lawrence": {
        "name": "Jennifer Lawrence",
        "birth": "August 15, 1990",
        "nationality": "American",
        "notable_films": ["Silver Linings Playbook", "The Hunger Games", "American Hustle", "Joy"],
        "awards": ["Academy Award", "BAFTA Award", "Golden Globe"],
        "bio": "Rose to global fame through The Hunger Games franchise and acclaimed dramatic roles.",
        "category": "A-List"
    },
    "natalie portman": {
        "name": "Natalie Portman",
        "birth": "June 9, 1981",
        "nationality": "Israeli-American",
        "notable_films": ["Black Swan", "V for Vendetta", "Jackie", "Thor"],
        "awards": ["Academy Award", "Golden Globe", "BAFTA Award"],
        "bio": "Harvard-educated actress known for intense dramatic performances and blockbuster roles.",
        "category": "Oscar Winners"
    },
    "zendaya": {
        "name": "Zendaya",
        "birth": "September 1, 1996",
        "nationality": "American",
        "notable_films": ["Dune", "Spider-Man: No Way Home", "Euphoria", "Challengers"],
        "awards": ["2 Emmy Awards", "Golden Globe"],
        "bio": "A defining star of her generation, equally successful in music, fashion, and film.",
        "category": "New Generation"
    },
    "florence pugh": {
        "name": "Florence Pugh",
        "birth": "January 3, 1996",
        "nationality": "British",
        "notable_films": ["Little Women", "Midsommar", "Oppenheimer", "Black Widow"],
        "awards": ["BAFTA Rising Star", "Oscar nomination"],
        "bio": "Acclaimed for bold, emotionally raw performances across indie and blockbuster films.",
        "category": "New Generation"
    },
    "margot robbie": {
        "name": "Margot Robbie",
        "birth": "July 2, 1990",
        "nationality": "Australian",
        "notable_films": ["Barbie", "I, Tonya", "The Wolf of Wall Street", "Suicide Squad"],
        "awards": ["Oscar nominations", "BAFTA nominations"],
        "bio": "Australian actress and producer known for both commercial hits and transformative dramatic roles.",
        "category": "A-List"
    },
    "charlize theron": {
        "name": "Charlize Theron",
        "birth": "August 7, 1975",
        "nationality": "South African-American",
        "notable_films": ["Monster", "Mad Max: Fury Road", "Atomic Blonde", "Bombshell"],
        "awards": ["Academy Award", "Golden Globe", "Screen Actors Guild Award"],
        "bio": "Known for physically demanding action roles and fearless dramatic transformations.",
        "category": "Oscar Winners"
    },
    "viola davis": {
        "name": "Viola Davis",
        "birth": "August 11, 1965",
        "nationality": "American",
        "notable_films": ["Fences", "The Help", "Ma Rainey's Black Bottom", "The Woman King"],
        "awards": ["Academy Award", "Emmy Award", "Tony Award"],
        "bio": "One of the few performers to achieve the 'Triple Crown of Acting' — Oscar, Emmy, and Tony.",
        "category": "Oscar Winners"
    },
}

CATEGORIES = ["A-List", "Oscar Winners", "New Generation"]
