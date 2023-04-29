from random import choices

modifiers = {
    "crit_rate":.1,
    "damage":.001,
}

print(choices(list(modifiers.keys()), k=3, weights=list(modifiers.values())))