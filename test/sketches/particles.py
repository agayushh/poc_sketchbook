import taichi as ti
from tolvera import Tolvera, run
from tolvera.cv import CV
def main(**kwargs):
    tv = Tolvera(**kwargs)
    # cv_instance = tv.cv()  # Use default webcam

    @tv.render
    def _():
        tv.cv()  # Process a frame from the camera
        tv.px.set(tv.cv().px)  # Return the pixels for rendering
        return tv.px
if __name__ == '__main__':
    run(main)

    