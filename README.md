# **mc-bismuth**
This projects adds a **robust, dynamic spell casting system**.

Use a **catalyst in your offhand** to cast a **spell** from an item in your **mainhand**.

For this data pack to work, the **vanilla ender eye behavior has been disabled**, so you can't use them to find the stronghold.

This library **shows cool down visually** using the [mc-silica](https://github.com/PuckiSilver/mc-silica) resource pack.

## **Prerequisites**
Make sure to use the [mc-silica](https://github.com/PuckiSilver/mc-silica) resource pack for your spells to **display the cool down**.

**Merge** this data pack **with your data pack** or use it as an external data pack.

## **Cool Down Calculation**
mc-bismuth uses `spell haste` and not a percentage cool down reduction. `spell haste` uses the same calculation that `ability haste` in [league of legends](https://leagueoflegends.fandom.com/wiki/Haste#Formula) uses and is therefore calculated like this:
```ini
remaining_cool_down = ( cool_down *  100 ) / ( 100 + spell_haste )
```

## **Register a new Spell**
### **Spell Dictionary Function**
First, you need to **create a spell dictionary function** in your pack that is used **detemine the spell**, that should be executed.
To create such a function you can look at the `template_spell_dictionary` function in [`main.bolt`](src/data/bismuth/modules/main.bolt).

### **Information Available**
When the **spell dictionary** is called and is calling your **spells**, you have access to the following information:

|Type||Description|
|---|---|---|
|Scoreboard|`.id_spell` `bismuth`|The **id** that you have assigned to your spell|
|Scoreboard|`@s` `bismuth.charge`|The time in ticks that right click **has been held** for|
|Scoreboard|`.finished` `bismuth`|If this score is 1, right click has been let go, meaning that the **"charge" has been completed**<br>0 otherwise|
|Context|`@s`|The spell dictionary **is executed** `as` and `at` the player that used the spell|

To put the executed spell on **cool down**, you can set the score `.cooldown` `bismuth` to the cool down in ticks and use the `bismuth:cool_down/set` function to apply it.

### **Register the Spell Dictionary Function**
Create the [spell dictionary function](#spell-dictionary-function) and **register it** to the `bismuth:spell_dictionary` function tag:

`/data/bismuth/tags/functions/spell_dictionary.json`
```json
{
    "values": [
        "<namespace>:<path to your function>"
    ]
}
```

## **Get the Items**
You can use the [`items.bolt`](src/data/bismuth/modules/items.bolt) file as a guide to **create loot tables**, that give yourself **catalyst- and spell items**.
If you use `beet` and `bolt` yourself, you can just copy the file and use it in your project.

Alernatively you could use a `give` command like the following ones:
```mcfunction
give @s minecraft:ender_eye{bismuth.catalyst:1b,CustomModelData:123456,magn:{spell_haste:15},AttributeModifiers:[{AttributeName:"generic.luck",Name:"tungsten.offhand",Amount:-0.000000000001,Operation:0,UUID:[I;12,42069,-0,11],Slot:"offhand"}]}
```
This command gives the player a catalyst, that is an `ender eye` with the `CustomModelData` 123456 and a `spell haste` of 15.

```mcfunction
give @s minecraft:leather_horse_armor{CustomModelData:654321,magn:{spell_id:42069},AttributeModifiers:[{AttributeName:"generic.luck",Name:"tungsten.mainhand",Amount:-0.000000000001,Operation:0,UUID:[I;12,42069,-0,10],Slot:"mainhand"}]}
```
This command gives the player a catalyst, that is an `ender eye` with the `CustomModelData` 654321 and a `spell id` of 42069.

## **Dependencies**
#### **Resource Pack**
The resource pack used to show the cool down visually. If you are not using this resource pack it will not look correct.
- [mc-silica](https://github.com/PuckiSilver/mc-silica)

#### **Included Libraries**
No need to download these, they are included in the final data pack.
- [mc-magnesium](https://github.com/PuckiSilver/mc-magnesium)
- [mc-tungsten](https://github.com/PuckiSilver/mc-tungsten)

#### **Development Environment**
This project is written using the following but if you just want to use this library, you don't need to download these.
- [beet](https://github.com/mcbeet/beet)
- [bolt](https://github.com/mcbeet/bolt)
- [mecha](https://github.com/mcbeet/mecha)

---
check me out on [Planet Minecraft](https://www.planetminecraft.com/member/puckisilver/)
