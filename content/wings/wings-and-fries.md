---
title: Wings + Fries
prices:
  - variable1: Medium
    variable2: "-"
    price: 57
  - variable1: Large
    variable2: "-"
    price: 67
tags:
  - Wings
  - Chicken
ingredients:
  - Chicken Wings
  - Fries
cookingmethods:
  - Fried
types:
  - Main
weight: 2
side_categories:
  - category_name: flavours
    display_name: Choose your flavours (2)
    config:
      minimum: 2
      maximum: 2
    items:
      - name: Original
        type: Regular
        price: 0
      - name: Honey BBQ
        type: Regular
        price: 0
      - name: Honey Mustard
        type: Regular
        price: 0
      - name: Lemon Pepper
        type: Regular
        price: 0
      - name: Guava BBQ
        type: Regular
        price: 0
      - name: Sweet + Spicy
        type: Regular
        price: 0
      - name: Tamarind
        type: Regular
        price: 0
  - category_name: extra_sauce
    display_name: Extra signature sauce
    config:
      minimum: 0
      maximum: 1
    items:
      - name: Extra signature sauce
        type: Premium
        price: 5
  - category_name: fries_upgrade_sweet_cassava
    display_name: Upgrade fries (sweet potato or cassava)
    config:
      minimum: 0
      maximum: 1
    items:
      - name: Sweet Potato Fries
        type: Regular
        price: 10
      - name: Cassava Fries
        type: Regular
        price: 10
  - category_name: fries_upgrade_wedges
    display_name: Upgrade to wedges
    config:
      minimum: 0
      maximum: 1
    items:
      - name: Seasoned Wedges
        type: Regular
        price: 8
---

Wings with fries. Any two flavours.
