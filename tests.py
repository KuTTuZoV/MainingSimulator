import computer
import json

motherBoardDefinition = "{" \
                        "   \"slots\" : " \
                        "           {" \
                        "               \"Процессор\": 2," \
                        "               \"Память\" : 4," \
                        "               \"Жесткий_диск\"   : 2," \
                        "               \"Видеокарта\" : 1" \
                        "           }" \
                        "}"

computer = computer.computer()

computer.setMotherBoard(json.loads(motherBoardDefinition)['slots'])
res = computer.addComponent("Процессор", {"Модель" : "Athlon", "Производительность" : 500})
res = computer.addComponent("Процессор", {"Модель" : "Athlon", "Производительность" : 500})

computer.removeComponent("Процессор", 1)

res = computer.addComponent("Процессор", {"Модель" : "Athlon", "Производительность" : 500})


performance = computer.calculatePerformance()

description = computer.toString()

#print(description)
