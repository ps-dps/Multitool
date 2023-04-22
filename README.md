# <img src="src/pack.png" height=25> **Multitool**

Do you **hate it** when your whole inventory is **cluttered by tools**?

Well, with this data pack you can **combine all the tools** into the **Multitool**.

## **Features**
If you look at a block, the Multitool **switches to a tool suited to break that block**.

When **sneaking** while looking at **tillable blocks**, the Multitool swaps to a **hoe**, so you can create fresh farmland.

You can **enchant** the Multitool!
It supports any enchantment that you can normally slap on a tool.

The tool **only loses durability 30% of the time** since it is made from 4 tools.<br>
This only increases the effective durability by 3.333 times and not 4 times.

Mutlitool even supports **resource packs**, like [this one](https://www.planetminecraft.com/texture-pack/multitool-halberds/) by [Crafterick](https://www.planetminecraft.com/member/craftrick/), it turns the **Multitool into a halberd**!

## **How to get**

![craft_stone_multitool](images/craft_stone_multitool.png)
![craft_diamond_multitool](images/craft_diamond_multitool.png)

To **craft** a Multitool, you just need to **combine all four types of tools** of the same material in the crafting grid.

You will see a `Knowledge Book` as the crafting result, take it out and it will get replaced by the Multitool.

If you are OP you can **give yourself the tool** by running the following command:
```mcfunction
loot give @s loot ps-multitool:{material}_multitool
```
Make sure to replace `{material}` with one of `golden`, `wooden`, `stone`, `diamond` or `netherite`.

## **Adding or removing a Multitool**
You can generate your **own Multitool** data pack simply by **configuring a config** and building it

> This also works for modded tools but note that **some mods break data packs** so I won't guarantee compatability or support

1. Install [Python](https://www.python.org/downloads/) and [beet](https://github.com/mcbeet/beet)<br>
    _If Python is allready installed, you should just be able to run `pip install beet` to install beet_

2. Clone or download the [GitHub repository](https://github.com/ps-dps/Multitool)

3. Add or remove `materials` in [`multitool_config.yml`](multitool_config.yml) and configure `overwrites`, for mods where a tool isn't following vanilla's naming scheme
    > You can easily find the namespace by looking at the item in your inventory after pressing **F3 + H**, it should be in the form `<namespace>:<material>_<tool>`

4. Move to this folder with a terminal and run `beet`, it should create a folder called `build` with your data pack in it

---
Check me out on other platforms:

<a href="https://github.com/PuckiSilver" target="_blank">
  <img src="https://github.githubassets.com/favicons/favicon-dark.svg" height="40" width="40"/>
</a>
<a href="https://modrinth.com/user/PuckiSilver" target="_blank">
  <img src="https://docs.modrinth.com/img/logo.svg" height="40" width="40"/>
</a>
<a href="https://www.planetminecraft.com/member/puckisilver" target="_blank">
  <img src="https://www.planetminecraft.com/images/layout/favicon-64.png" height="40" width="40"/>
</a>
