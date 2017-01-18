import engine

e = engine.Engine()
e.export_level("Levels/demo")
e.import_level("Levels/demo")
e.run()
