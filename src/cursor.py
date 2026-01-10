cursor = ">"

gutter = len(cursor)

x=0
y=0

def draw_cursor(
        x = 0, 
        y = 0
    ):

    print(f"X = {x}")
    print(f"Y = {y}")
    print(cursor, end = "")
    input()

if __name__ == "__main__":
    import display

    display.clear()
    draw_cursor()

    input("END")