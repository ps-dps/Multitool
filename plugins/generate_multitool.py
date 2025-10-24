from beet import Advancement, Context, FunctionTag, Function, ItemModifier, ItemTag, LootTable, Predicate, BlockTag, Recipe, Texture
import yaml
try:
    from PIL import Image
except:
    ...

def beet_default(ctx: Context):
    config_path = ctx.meta.get('multitool')
    if config_path == None:
        print('[Multitool] Missing Multitool Config, aborting')
        return
    with open(config_path) as stream:
        try:
            config = yaml.safe_load(stream)
        except:
            print('[Multitool] Can\'t read Config')
            return
    if not generate_from_config(ctx, config): return
    add_lantern_load(ctx)
    add_multitool_base(ctx)

def add_lantern_load(ctx: Context):
    ctx.data["minecraft:load"] = FunctionTag({"values": ["#load:_private/load"]})
    ctx.data["load:_private/load"] = FunctionTag(
        {
            "values": [
                "#load:_private/init",
                {"id": "#load:pre_load", "required": False},
                {"id": "#load:load", "required": False},
                {"id": "#load:post_load", "required": False},
            ]
        }
    )

    ctx.data["load:_private/init"] = FunctionTag({"values": ["load:_private/init"]})
    ctx.data["load:_private/init"] = Function(
        [
            "scoreboard objectives add load.status dummy",
            "scoreboard players reset * load.status",
        ]
    )

def add_multitool_base(ctx: Context):
    try:
        ctx.data.icon = Texture(Image.open('images/pack.png'))
    except:
        ...
    ctx.data.function_tags["load:load"] = FunctionTag({"values":["ps-multitool:load"]})
    ctx.data.functions["ps-multitool:load"] = Function([
        "scoreboard objectives add ps-multitool dummy",
        "schedule function ps-multitool:tick 1t replace",
    ])
    ctx.data.functions["ps-multitool:tick"] = Function([
        "schedule function ps-multitool:tick 1t replace",
        "execute as @a[predicate=ps-multitool:has_multitool] at @s anchored eyes positioned ^ ^ ^ run function ps-multitool:multitool_tick",
    ])
    ctx.data.functions["ps-multitool:multitool_tick"] = Function([
        "execute unless score .ray_range ps-multitool matches 1.. run scoreboard players set .ray_range ps-multitool 17",
        "scoreboard players remove .ray_range ps-multitool 1",
        "execute if block ~ ~ ~ #minecraft:mineable/axe unless predicate ps-multitool:sneak_transform/axe_to_shovel unless items entity @s weapon.mainhand #ps-multitool:tool/axe run item modify entity @s weapon.mainhand ps-multitool:swap/axe",
        "execute if predicate ps-multitool:sneak_transform/axe_to_shovel unless items entity @s weapon.mainhand #ps-multitool:tool/shovel run item modify entity @s weapon.mainhand ps-multitool:swap/shovel",
        "execute if block ~ ~ ~ #minecraft:mineable/hoe unless items entity @s weapon.mainhand #ps-multitool:tool/hoe run item modify entity @s weapon.mainhand ps-multitool:swap/hoe",
        "execute if block ~ ~ ~ #minecraft:mineable/pickaxe unless predicate ps-multitool:sneak_transform/pickaxe_to_axe unless items entity @s weapon.mainhand #ps-multitool:tool/pickaxe run item modify entity @s weapon.mainhand ps-multitool:swap/pickaxe",
        "execute if predicate ps-multitool:sneak_transform/pickaxe_to_axe unless items entity @s weapon.mainhand #ps-multitool:tool/axe run item modify entity @s weapon.mainhand ps-multitool:swap/axe",
        "execute if block ~ ~ ~ #minecraft:mineable/shovel unless predicate ps-multitool:sneak_transform/shovel_to_hoe unless items entity @s weapon.mainhand #ps-multitool:tool/shovel run item modify entity @s weapon.mainhand ps-multitool:swap/shovel",
        "execute if predicate ps-multitool:sneak_transform/shovel_to_hoe unless items entity @s weapon.mainhand #ps-multitool:tool/hoe run item modify entity @s weapon.mainhand ps-multitool:swap/hoe",
        "execute if score .ray_range ps-multitool matches 1.. unless block ~ ~ ~ #ps-multitool:mineable positioned ^ ^ ^0.3 run function ps-multitool:multitool_tick",
    ])
    ctx.data.predicates["ps-multitool:has_multitool"] = Predicate(
        { "condition": "minecraft:entity_properties", "entity": "this", "predicate": {
            "equipment": { "mainhand": {
                "items": "#ps-multitool:tools",
                "predicates": { "minecraft:custom_data": { "ps-multitool": 1 }}
    }}}})
    ctx.data.predicates["ps-multitool:sneak_transform/shovel_to_hoe"] = Predicate({
        "condition": "minecraft:all_of", "terms": [
            { "condition": "minecraft:entity_properties", "entity": "this", "predicate": {
                "flags": { "is_sneaking": True }}},
            { "condition": "minecraft:location_check", "predicate": {
                "block": { "blocks": "#ps-multitool:tillable" }}
    }]})
    ctx.data.predicates["ps-multitool:sneak_transform/axe_to_shovel"] = Predicate({
        "condition": "minecraft:all_of", "terms": [
            { "condition": "minecraft:entity_properties", "entity": "this", "predicate": {
                "flags": { "is_sneaking": True }}},
            { "condition": "minecraft:location_check", "predicate": {
                "block": { "blocks": "#minecraft:campfires" }}
    }]})
    ctx.data.predicates["ps-multitool:sneak_transform/pickaxe_to_axe"] = Predicate({
        "condition": "minecraft:all_of", "terms": [
            { "condition": "minecraft:entity_properties", "entity": "this", "predicate": {
                "flags": { "is_sneaking": True }}},
            { "condition": "minecraft:location_check", "predicate": {
                "block": { "blocks": "#ps-multitool:scrapeable" }}
    }]})
    ctx.data.block_tags["ps-multitool:tillable"] = BlockTag({ "values": [
        { "required": False, "id": "minecraft:grass_block" },
        { "required": False, "id": "minecraft:coarse_dirt" },
        { "required": False, "id": "minecraft:rooted_dirt" },
        { "required": False, "id": "minecraft:dirt_path" },
        { "required": False, "id": "minecraft:farmland" },
        { "required": False, "id": "minecraft:dirt" },
    ]})
    ctx.data.block_tags["ps-multitool:mineable"] = BlockTag({ "values": [
        { "required": False, "id": "#minecraft:mineable/pickaxe" },
        { "required": False, "id": "#minecraft:mineable/shovel" },
        { "required": False, "id": "#minecraft:mineable/axe" },
        { "required": False, "id": "#minecraft:mineable/hoe" },
    ]})
    ctx.data.block_tags["ps-multitool:scrapeable"] = BlockTag({ "values": [
        { "required": False, "id": id } for id in ["#minecraft:copper", "#minecraft:copper_chests", "#minecraft:copper_golem_statues", "minecraft:lightning_rod", "minecraft:exposed_lightning_rod", "minecraft:weathered_lightning_rod", "minecraft:oxidized_lightning_rod", "minecraft:waxed_lightning_rod", "minecraft:waxed_exposed_lightning_rod", "minecraft:waxed_weathered_lightning_rod", "minecraft:waxed_oxidized_lightning_rod", "minecraft:copper_lantern", "minecraft:exposed_copper_lantern", "minecraft:weathered_copper_lantern", "minecraft:oxidized_copper_lantern", "minecraft:waxed_copper_lantern", "minecraft:waxed_exposed_copper_lantern", "minecraft:waxed_weathered_copper_lantern", "minecraft:waxed_oxidized_copper_lantern", "minecraft:copper_bars", "minecraft:exposed_copper_bars", "minecraft:weathered_copper_bars", "minecraft:oxidized_copper_bars", "minecraft:waxed_copper_bars", "minecraft:waxed_exposed_copper_bars", "minecraft:waxed_weathered_copper_bars", "minecraft:waxed_oxidized_copper_bars", "minecraft:copper_trapdoor", "minecraft:exposed_copper_trapdoor", "minecraft:weathered_copper_trapdoor", "minecraft:oxidized_copper_trapdoor", "minecraft:waxed_copper_trapdoor", "minecraft:waxed_exposed_copper_trapdoor", "minecraft:waxed_weathered_copper_trapdoor", "minecraft:waxed_oxidized_copper_trapdoor", "minecraft:copper_chain", "minecraft:exposed_copper_chain", "minecraft:weathered_copper_chain", "minecraft:oxidized_copper_chain", "minecraft:waxed_copper_chain", "minecraft:waxed_exposed_copper_chain", "minecraft:waxed_weathered_copper_chain", "minecraft:waxed_oxidized_copper_chain", "minecraft:copper_door", "minecraft:exposed_copper_door", "minecraft:weathered_copper_door", "minecraft:oxidized_copper_door", "minecraft:waxed_copper_door", "minecraft:waxed_exposed_copper_door", "minecraft:waxed_weathered_copper_door", "minecraft:waxed_oxidized_copper_door", "minecraft:cut_copper_slab", "minecraft:exposed_cut_copper_slab", "minecraft:weathered_cut_copper_slab", "minecraft:oxidized_cut_copper_slab", "minecraft:waxed_cut_copper_slab", "minecraft:waxed_exposed_cut_copper_slab", "minecraft:waxed_weathered_cut_copper_slab", "minecraft:waxed_oxidized_cut_copper_slab", "minecraft:cut_copper_stairs", "minecraft:exposed_cut_copper_stairs", "minecraft:weathered_cut_copper_stairs", "minecraft:oxidized_cut_copper_stairs", "minecraft:waxed_cut_copper_stairs", "minecraft:waxed_exposed_cut_copper_stairs", "minecraft:waxed_weathered_cut_copper_stairs", "minecraft:waxed_oxidized_cut_copper_stairs", "minecraft:copper_grate", "minecraft:exposed_copper_grate", "minecraft:weathered_copper_grate", "minecraft:oxidized_copper_grate", "minecraft:waxed_copper_grate", "minecraft:waxed_exposed_copper_grate", "minecraft:waxed_weathered_copper_grate", "minecraft:waxed_oxidized_copper_grate", "minecraft:copper_bulb", "minecraft:exposed_copper_bulb", "minecraft:weathered_copper_bulb", "minecraft:oxidized_copper_bulb", "minecraft:waxed_copper_bulb", "minecraft:waxed_exposed_copper_bulb", "minecraft:waxed_weathered_copper_bulb", "minecraft:waxed_oxidized_copper_bulb", "minecraft:chiseled_copper", "minecraft:exposed_chiseled_copper", "minecraft:weathered_chiseled_copper", "minecraft:oxidized_chiseled_copper", "minecraft:waxed_chiseled_copper", "minecraft:waxed_exposed_chiseled_copper", "minecraft:waxed_weathered_chiseled_copper", "minecraft:waxed_oxidized_chiseled_copper", "minecraft:cut_copper", "minecraft:exposed_cut_copper", "minecraft:weathered_cut_copper", "minecraft:oxidized_cut_copper", "minecraft:waxed_cut_copper", "minecraft:waxed_exposed_cut_copper", "minecraft:waxed_weathered_cut_copper", "minecraft:waxed_oxidized_cut_copper"]
    ]})

def generate_from_config(ctx: Context, cfg: dict):
    tools = ["axe", "hoe", "pickaxe", "shovel"]
    materials = cfg.get('materials')
    if not materials:
        print('[Multitool] The config doesn\'t specify any materials')
        return False
    for material in materials:
        if len(material["m"].split(':')) != 2:
            print('[Multitool] Materials need to be in the form {namespace}:{material["m"]}')
            return False
    overwrites = cfg.get('overwrites', {})
    for key, value in overwrites.items():
        all_tools = [f'{material["m"]}_{tool}' for material in materials for tool in tools]
        if not key in all_tools:
            print('[Multitool] The key of each overwrite has to be {namespace}:{material["m"]}_{tool}')
            return False
        if value in all_tools:
            print('[Multitool] The value of each overwrite can\'t be {namespace}:{material["m"]}_{tool}')
            return False
        if len(value.split(':')) != 2:
            print('[Multitool] Overwrites need to be in the form {namespace}:{material["m"]}')
            return False

    for material in materials:
        material_name = material["m"].split(':')[1]
        ctx.data.item_tags[f'ps-multitool:material/{material_name}'] = ItemTag(
            {"values": [{'id':f'{overwrites.get(material["m"]+"_"+tool,material["m"]+"_"+tool)}','required':False} for tool in tools]})
        rules = [{
            "blocks": f'#minecraft:mineable/{tool}',
            "correct_for_drops": True,
            "speed": material["s"],
        } for tool in tools]
        rules.insert(0, {
            "blocks": material.get("incorrect","#minecraft:incorrect_for_"+material_name+"_tool"),
            "correct_for_drops": False,
        })
        ctx.data.recipes[f'ps-multitool:{material_name}_multitool'] = Recipe({
            "type": "minecraft:crafting_shapeless",
            "category": "equipment",
            "ingredients": [f'{overwrites.get(material["m"]+"_"+tool,material["m"]+"_"+tool)}' for tool in tools ],
            "result": {
                "id": f'{overwrites.get(material["m"]+"_pickaxe",material["m"]+"_pickaxe")}',
                "components": {
                    "minecraft:custom_data": { "ps-multitool": 1 },
                    "minecraft:item_name": [
                        { "text": "M", "color": "#00ff00", "italic": False },
                        { "text": "u", "color": "#00e093", "italic": False },
                        { "text": "l", "color": "#00baca", "italic": False },
                        { "text": "t", "color": "#008fca", "italic": False },
                        { "text": "i", "color": "#00639a", "italic": False },
                        { "text": "t", "color": "#008fca", "italic": False },
                        { "text": "o", "color": "#00baca", "italic": False },
                        { "text": "o", "color": "#00e093", "italic": False },
                        { "text": "l", "color": "#00ff00", "italic": False }
                    ],
                    "minecraft:max_damage": material["d"],
                    "minecraft:tool": { "rules": rules },
                }
            }})
        ctx.data.advancements[f'ps-multitool:unlock_{material_name}_multitool_recipe'] = Advancement({
            "criteria": { "requirement": {
                "trigger": "minecraft:inventory_changed",
                "conditions": { "items": [{ "items": f'#ps-multitool:material/{material_name}' }]}
            }},
            "rewards": { "recipes": [ f'ps-multitool:{material_name}_multitool' ]}
        })

    for tool in tools:
        ctx.data.item_modifiers[f'ps-multitool:swap/{tool}'] = ItemModifier([
            {
                "function": "minecraft:set_item",
                "item": material["m"]+"_"+tool,
                "conditions": [{
                    "condition": "minecraft:entity_properties",
                    "entity": "this",
                    "predicate": { "equipment": {
                        "mainhand": { "items": f'#ps-multitool:material/{material["m"].split(":")[1]}' }
                    }}
                }]
            } for material in materials
        ])
        ctx.data.item_tags[f'ps-multitool:tool/{tool}'] = ItemTag(
            {"values": [
                {
                    'id':f'{overwrites.get(material["m"]+"_"+tool,material["m"]+"_"+tool)}',
                    'required':False
                } for material in materials
            ]})

    ctx.data.item_tags['ps-multitool:tools'] = ItemTag({ "values": [
        { "id": f'#ps-multitool:tool/{tool}', "required": False } for tool in tools ]})

    netherite_material = [m for m in materials if m["m"] == "minecraft:netherite"][0]
    ctx.data.item_modifiers["ps-multitool:smithing/upgrade_to_netherite"] = ItemModifier({
        "function": "minecraft:set_components",
        "components": {
            "minecraft:max_damage": netherite_material["d"],
            "minecraft:tool": { "rules": [{
                "blocks": netherite_material.get("incorrect","#minecraft:incorrect_for_netherite_tool"),
                "correct_for_drops": False,
            }] + [{
                "blocks": f'#minecraft:mineable/{tool}',
                "correct_for_drops": True,
                "speed": netherite_material["s"],
            } for tool in tools]}
        }
    })

    for tool in tools:
        ctx.data.advancements[f'ps-multitool:smithing/{tool}'] = Advancement({
            "criteria": { "requirement": {
                "trigger": "minecraft:recipe_crafted",
                "conditions": {
                    "recipe_id": f'minecraft:netherite_{tool}_smithing',
                    "ingredients": [{
                        "items": f'minecraft:diamond_{tool}',
                        "predicates": { "minecraft:custom_data": { "ps-multitool": 1 }}
                    }]
            }}},
            "rewards": { "function": "ps-multitool:smithing/craft" }
        })
    ctx.data.functions["ps-multitool:smithing/craft"] = Function(
        [f'advancement revoke @s only ps-multitool:smithing/{tool}' for tool in tools] + [
        "execute if items entity @s player.cursor #ps-multitool:material/netherite[custom_data~{ps-multitool:1b},max_damage=4683] run " +
            "return run item modify entity @s player.cursor ps-multitool:smithing/upgrade_to_netherite",
        "execute if items entity @s hotbar.* #ps-multitool:material/netherite[custom_data~{ps-multitool:1b},max_damage=4683] run " +
            "return run function ps-multitool:smithing/replace_in_hotbar",
        "execute if items entity @s inventory.* #ps-multitool:material/netherite[custom_data~{ps-multitool:1b},max_damage=4683] run " +
            "return run function ps-multitool:smithing/replace_in_inventory",
        "tellraw @s {\"text\":\"Coudn't convert Multitool to netherite, do NOT drop the output out of the smithing table!\",\"color\":\"red\"}",
    ])
    ctx.data.functions["ps-multitool:smithing/replace_in_hotbar"] = Function([
        "execute if items entity @s hotbar."+str(i)+" #ps-multitool:material/netherite[custom_data~{ps-multitool:1b},max_damage=4683] run return run item modify entity @s hotbar."+str(i)+" ps-multitool:smithing/upgrade_to_netherite"
        for i in range(9)
    ])
    ctx.data.functions["ps-multitool:smithing/replace_in_inventory"] = Function([
        "execute if items entity @s inventory."+str(i)+" #ps-multitool:material/netherite[custom_data~{ps-multitool:1b},max_damage=4683] run return run item modify entity @s inventory."+str(i)+" ps-multitool:smithing/upgrade_to_netherite"
        for i in range(27)
    ])

    return True
