import multiprocessing
import orgin
import Camera


if __name__ == '__main__':
    print("Main begin!")
    with multiprocessing.Manager() as manager:
        result = manager.list([None])
        p1 = multiprocessing.Process(target=Camera.collect, args=(result,))
        p2 = multiprocessing.Process(target=orgin.game, args=(result,))

        p1.start()
        p2.start()
        #p2.join()
        p2.join()
