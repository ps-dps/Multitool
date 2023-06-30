from beet import Advancement, Context, ExtraPin, FunctionTag, Function, ItemModifier, ItemTag, LootTable, PngFile, Predicate, BlockTag, Recipe, Texture
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
        "scoreboard players reset @a ps-multitool",
        "execute as @a[predicate=ps-multitool:has_multitool] at @s anchored eyes positioned ^ ^ ^ run function ps-multitool:multitool_tick",
    ])
    ctx.data.functions["ps-multitool:multitool_tick"] = Function([
        "scoreboard players set @s ps-multitool 1",
        "execute unless score .ray_range ps-multitool matches 1.. run scoreboard players set .ray_range ps-multitool 16",
        "scoreboard players remove .ray_range ps-multitool 1",
        "execute if block ~ ~ ~ #minecraft:mineable/axe unless predicate ps-multitool:tool/axe run loot replace entity @s weapon.mainhand loot ps-multitool:swap/axe",
        "execute if block ~ ~ ~ #minecraft:mineable/hoe unless predicate ps-multitool:tool/hoe run loot replace entity @s weapon.mainhand loot ps-multitool:swap/hoe",
        "execute if block ~ ~ ~ #minecraft:mineable/pickaxe unless predicate ps-multitool:tool/pickaxe run loot replace entity @s weapon.mainhand loot ps-multitool:swap/pickaxe",
        "execute if block ~ ~ ~ #minecraft:mineable/shovel unless predicate ps-multitool:should_hoe unless predicate ps-multitool:tool/shovel run loot replace entity @s weapon.mainhand loot ps-multitool:swap/shovel",
        "execute if predicate ps-multitool:should_hoe unless predicate ps-multitool:tool/hoe run loot replace entity @s weapon.mainhand loot ps-multitool:swap/hoe",
        "execute if score .ray_range ps-multitool matches 1.. unless block ~ ~ ~ #minecraft:mineable/axe unless block ~ ~ ~ #minecraft:mineable/hoe unless block ~ ~ ~ #minecraft:mineable/pickaxe unless block ~ ~ ~ #minecraft:mineable/shovel positioned ^ ^ ^0.3 run function ps-multitool:multitool_tick",
    ])
    ctx.data.functions["ps-multitool:keep_dura"] = Function([
        "advancement revoke @s only ps-multitool:keep_dura",
        "item modify entity @s weapon.mainhand ps-multitool:keep_dura",
    ])
    ctx.data.item_modifiers["ps-multitool:keep_dura"] = ItemModifier(
        {"function": "minecraft:copy_nbt","source": "this","ops": [{"source": "SelectedItem.tag.Damage","target": "Damage","op": "merge"}]}
    )
    ctx.data.predicates["ps-multitool:has_multitool"] = Predicate({
        "condition": "minecraft:any_of", "terms": [{ "condition": "minecraft:entity_properties", "entity": "this", "predicate": {
            "equipment": { "mainhand": {
                "tag": "ps-multitool:tools",
                "nbt": "{ps-multitool:1b}" }}}
    }]})
    ctx.data.predicates["ps-multitool:repair_chance"] = Predicate({
        "condition": "minecraft:random_chance", "chance": 0.7
    })
    ctx.data.predicates["ps-multitool:should_hoe"] = Predicate("""[
        { \"condition\": \"minecraft:entity_properties\", \"entity\": \"this\", \"predicate\": {
            \"flags\": { \"is_sneaking\": true }}},
        { \"condition\": \"minecraft:location_check\", \"predicate\": {
            \"block\": { \"tag\": \"ps-multitool:tillable\" }}
    }]""")
    ctx.data.block_tags["ps-multitool:tillable"] = BlockTag({ "values": [
        { "id": "minecraft:grass_block", "required": False },
        { "id": "minecraft:dirt", "required": False },
        { "id": "minecraft:farmland", "required": False },
        { "id": "minecraft:dirt_path", "required": False },
        { "id": "minecraft:coarse_dirt", "required": False },
        { "id": "minecraft:rooted_dirt", "required": False }]
    })

def generate_from_config(ctx: Context, cfg: dict):
    tools = ["axe", "hoe", "pickaxe", "shovel"]
    materials = cfg.get('materials')
    if not materials:
        print('[Multitool] The config doesn\'t specify any materials')
        return False
    for material in materials:
        if len(material.split(':')) != 2:
            print('[Multitool] Materials need to be in the form {namespace}:{material}')
            return False
    overwrites = cfg.get('overwrites', {})
    for key, value in overwrites.items():
        all_tools = [f'{material}_{tool}' for material in materials for tool in tools]
        if not key in all_tools:
            print('[Multitool] The key of each overwrite has to be {namespace}:{material}_{tool}')
            return False
        if value in all_tools:
            print('[Multitool] The value of each overwrite can\'t be {namespace}:{material}_{tool}')
            return False
        if len(value.split(':')) != 2:
            print('[Multitool] Overwrites need to be in the form {namespace}:{material}')
            return False

    for material in materials:
        ctx.data.functions[f'ps-multitool:craft/{material.split(":")[1]}_multitool'] = Function([
            f'advancement revoke @s only ps-multitool:craft/{material.split(":")[1]}_multitool',
            f'recipe take @s ps-multitool:{material.split(":")[1]}_multitool',
            'clear @s knowledge_book',
            f'loot give @s loot ps-multitool:{material.split(":")[1]}_multitool',
        ])
        ctx.data.item_tags[f'ps-multitool:material/{material.split(":")[1]}'] = ItemTag(
            {"values": [{'id':f'{overwrites.get(material+"_"+tool,material+"_"+tool)}','required':False} for tool in tools]})
        ctx.data.recipes[f'ps-multitool:{material.split(":")[1]}_multitool'] = Recipe({ "type": "minecraft:crafting_shapeless",
            "ingredients": [{ "item": f'{overwrites.get(material+"_"+tool,material+"_"+tool)}' } for tool in tools ],
            "result": { "item": "minecraft:knowledge_book" }})
        ctx.data.loot_tables[f'ps-multitool:{material.split(":")[1]}_multitool'] = LootTable({ "pools": [{ "rolls": 1, "entries": [{ "type": "minecraft:item",
            "name": f'{overwrites.get(material+"_pickaxe",material+"_pickaxe")}',
            "functions": [{
                "function": "minecraft:set_nbt",
                "tag": "{ps-multitool:1b,CustomModelData:74201}" },
            {
                "function": "minecraft:set_lore",
                "lore": [[
                    { "text": "M", "color": "#00ff00", "italic": False },
                    { "text": "u", "color": "#00e093", "italic": False },
                    { "text": "l", "color": "#00baca", "italic": False },
                    { "text": "t", "color": "#008fca", "italic": False },
                    { "text": "i", "color": "#00639a", "italic": False },
                    { "text": "t", "color": "#008fca", "italic": False },
                    { "text": "o", "color": "#00baca", "italic": False },
                    { "text": "o", "color": "#00e093", "italic": False },
                    { "text": "l", "color": "#00ff00", "italic": False },
        ]]}]}]}]})
        ctx.data.advancements[f'ps-multitool:craft/{material.split(":")[1]}_multitool'] = Advancement({ "criteria": { "requirement": { "trigger": "minecraft:recipe_unlocked", "conditions": {
            "recipe": f'ps-multitool:{material.split(":")[1]}_multitool' }}},
            "rewards": { "function": f'ps-multitool:craft/{material.split(":")[1]}_multitool' }})

    for tool in tools:
        ctx.data.loot_tables[f'ps-multitool:swap/{tool}'] = LootTable(
            {"pools":[{"rolls":1,"entries":[{
                "type": "minecraft:item",
                "name": f'{overwrites.get(material+"_"+tool,material+"_"+tool)}',
                "conditions": [{ "condition": "minecraft:entity_properties", "entity": "this", "predicate": { "equipment": {
                    "mainhand": {
                        "tag": f'ps-multitool:material/{material.split(":")[1]}' }}}}],
                "functions": [{ "function": "minecraft:copy_nbt", "source": "this", "ops": [{
                    "source": "SelectedItem.tag",
                    "target": "{}",
                    "op": "merge" }]}]
            } for material in materials ]}]})
        ctx.data.item_tags[f'ps-multitool:tool/{tool}'] = ItemTag(
            {"values": [{'id':f'{overwrites.get(material+"_"+tool,material+"_"+tool)}','required':False} for material in materials]})
        ctx.data.predicates[f'ps-multitool:tool/{tool}'] = Predicate({
            "condition": "minecraft:any_of", "terms": [{ "condition": "minecraft:entity_properties", "entity": "this", "predicate": { "tool": "minecraft:player", "equipment": {
                "mainhand": {
                    "tag": f'ps-multitool:tool/{tool}',
                    "nbt": "{ps-multitool:1b}" }}}}]})

    ctx.data.item_tags['ps-multitool:tools'] = ItemTag({ "values": [
        { "id": f'#ps-multitool:tool/{tool}', "required": False } for tool in tools ]})
    return True
