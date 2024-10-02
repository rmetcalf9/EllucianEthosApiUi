import MainMenu
import EllucianEthosPythonClient

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Start of EllucianEthosAPIUi")
    print(" Using library version", EllucianEthosPythonClient.__version__)

    mainMenu = MainMenu.MainMenu()
    mainMenu.run()

