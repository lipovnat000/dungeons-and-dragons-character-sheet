CLASSES = {
    "Rogue": {
        "hit_die": 8,
        "saving_throws": ["dex", "int"],

        "features": {
            1: [
                {"name": "Expertise", "type": "text"},
                {"name": "Sneak Attack", "type": "mechanic",
                 "dice_per_level": {1: "1d6"}}
            ],
            2: [
                {"name": "Cunning Action", "type": "text"}
            ],
            3: [
                {"name": "Sneak Attack", "type": "mechanic",
                 "dice_per_level": {3: "2d6"}}
            ],
            5: [
                {"name": "Sneak Attack", "type": "mechanic",
                 "dice_per_level": {5: "3d6"}}
            ]
        }
    },

    "Sorcerer": {
        "hit_die": 6,
        "saving_throws": ["con", "cha"],

        "features": {
            1: [
                {"name": "Spellcasting", "type": "text"},
                {"name": "Sorcerous Origin", "type": "text"}
            ],
            2: [
                {"name": "Font of Magic", "type": "text"}
            ],
            3: [
                {"name": "Metamagic", "type": "text"}
            ]
        }
    }
}