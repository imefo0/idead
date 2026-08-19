import core
# добавляет все описания и использования команд (helper.*)

data = core.load()

data = core.add(data, "helper", {
    "using": "idead <command> <args> <flags>",
    "about": "ideeeeead",
    "subcmds": {
        "init": {
            "using": "idead init",
            "about": "prepare the environment: create all the necessary folders and configuration files"
        },
        "test": {
            "using": "idead test",
            "about": "run all tests and show progress"
        },
        "new": {
            "using": "idead new {idea} <name> <desc>",
            "about": "create new entity: idea, post, task, or guide",
            "subcmds": {
                "idea": {
                    "using": "idead new idea <name> <desc>",
                    "about": "create a new idea with name and description"
                }
            }
        },
        "remove": {
            "using": "idead remove {idea} [--date YYMMDD] [--time HHMM] [--name <name>] [--uuid <uuid6>]",
            "about": "remove entity by type and filters",
            "subcmds": {
                "idea": {
                    "using": "idead remove idea [--date YYMMDD] [--time HHMM] [--name <name>] [--uuid <uuid6>]",
                    "about": "remove an idea by date, time, name, or UUID",
                    "flags": {
                        "--date": {
                            "using": "idead remove idea --date <YYMMDD>",
                            "about": "filter ideas by date (YYYYMMDD)"
                        },
                        "--time": {
                            "using": "idead remove idea --time <HHMM>",
                            "about": "filter ideas by time (HHMM)"
                        },
                        "--name": {
                            "using": "idead remove idea --name <name>",
                            "about": "filter ideas by name (exact match)"
                        },
                        "--uuid": {
                            "using": "idead remove idea --uuid <uuid6>",
                            "about": "filter idea by UUID (first 6 chars)"
                        }
                    }
                }
            }
        },
        "search": {
            "using": "idead search {idea} [--name <name>]",
            "about": "search for entities by text",
            "subcmds": {
                "idea": {
                    "using": "idead search idea [--name <name>]",
                    "about": "search for ideas by name (trigram + Jaccard)",
                    "flags": {
                        "--name": {
                            "using": "idead search idea --name <name>",
                            "about": "search ideas by name using trigram similarity"
                        }
                    }
                }
            }
        },
        "list": {
            "using": "idead list {idea}",
            "about": "list all entities",
            "subcmds": {
                "idea": {
                    "using": "idead list idea",
                    "about": "list all ideas in a table"
                }
            }
        },
        "config": {
            "using": "idead config {reset | update | <path> get | <path> set <value> | <path> reset}",
            "about": "manage configuration: get, set, reset",
            "subcmds": {
                "reset": {
                    "using": "idead config reset",
                    "about": "reset ENTIRE config to defaults (irreversible!)"
                },
                "update": {
                    "using": "idead config update",
                    "about": "migrate config to the latest version"
                },
                "arg": {
                    "reset": {
                        "using": "idead <path> reset",
                        "about": "reset a specific config field to its default value"
                    },
                    "get": {
                        "using": "idead <path> get",
                        "about": "get the value of a specific config field"
                    },
                    "set": {
                        "using": "idead <path> set <value>",
                        "about": "set a specific config field to a new value (auto-casts type)"
                    }
                }
            }
        }
    }
})

data = core.ver(data, "1.3")

print("1.2 -> 1.3:")
print("- new: helper.*")

core.save(data)
