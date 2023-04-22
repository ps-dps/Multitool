from beet import Context, FunctionTag, Function, ItemModifier, Predicate, BlockTag
import yaml

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
    print(config)
    return
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
    ctx.data.item_modifiers["ps-multitool:has_multitool"] = ItemModifier(
        {"function": "minecraft:copy_nbt","source": "this","ops": [{"source": "SelectedItem.tag.Damage","target": "Damage","op": "merge"}]}
    )
    ctx.data.predicates["ps-multitool:keep_dura"] = Predicate({
        "condition": "minecraft:alternative", "terms": [{ "condition": "minecraft:entity_properties", "entity": "this", "predicate": { "tool": "minecraft:player",
            "equipment": { "mainhand": {
                "tag": "ps-multitool:tools",
                "nbt": "{ps-multitool:1b}" }}}
    }]})
    ctx.data.predicates["ps-multitool:repair_chance"] = Predicate({
        "condition": "minecraft:random_chance", "chance": 0.7
    })
    ctx.data.predicates["ps-multitool:should_hoe"] = Predicate([
        { "condition": "minecraft:entity_properties", "entity": "this", "predicate": {
            "flags": { "is_sneaking": True }}},
        { "condition": "minecraft:location_check", "predicate": {
            "block": { "tag": "ps-multitool:tillable" }}
    }])
    ctx.data.predicates["ps-multitool:block_tag"] = BlockTag({ "values": [
        { "id": "minecraft:grass_block", "required": False },
        { "id": "minecraft:dirt", "required": False },
        { "id": "minecraft:farmland", "required": False },
        { "id": "minecraft:dirt_path", "required": False },
        { "id": "minecraft:coarse_dirt", "required": False },
        { "id": "minecraft:rooted_dirt", "required": False }]
    })

def generate_from_config(ctx: Context, cfg: dict):
    tools = ["axe", "hoe", "pickaxe", "shovel"]
    for material in cfg['materials']:
        ctx.data.functions[f'ps-multitool:craft/{material}_multitool'] = Function([
            f'advancement revoke @s only ps-multitool:craft/{material}_multitool',
            f'recipe take @s ps-multitool:{material}_multitool',
            'clear @s knowledge_book',
            f'loot give @s loot ps-multitool:{material}_multitool',
        ])
    for tool in tools:
        ...
