import numpy as np

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y


def get_homography(s0, s1, s2, s3, t0, t1, t2, t3):

    x0s = s0.x
    y0s = s0.y
    x0t = t0.x
    y0t = t0.y

    x1s = s1.x
    y1s = s1.y
    x1t = t1.x
    y1t = t1.y

    x2s = s2.x
    y2s = s2.y
    x2t = t2.x
    y2t = t2.y

    x3s = s3.x
    y3s = s3.y
    x3t = t3.x
    y3t = t3.y

    # linear constraints betwixt source and target
    A = np.matrix([
            [x0s, y0s, 1, 0, 0, 0, -x0t * x0s, -x0t * y0s],
            [0, 0, 0, x0s, y0s, 1, -y0t * x0s, -y0t * y0s],
            [x1s, y1s, 1, 0, 0, 0, -x1t * x1s, -x1t * y1s],
            [0, 0, 0, x1s, y1s, 1, -y1t * x1s, -y1t * y1s],
            [x2s, y2s, 1, 0, 0, 0, -x2t * x2s, -x2t * y2s],
            [0, 0, 0, x2s, y2s, 1, -y2t * x2s, -y2t * y2s],
            [x3s, y3s, 1, 0, 0, 0, -x3t * x3s, -x3t * y3s],
            [0, 0, 0, x3s, y3s, 1, -y3t * x3s, -y3t * y3s]
        ])

    # column vector of target coords
    b = np.array([
            [x0t],
            [y0t],
            [x1t],
            [y1t],
            [x2t],
            [y2t],
            [x3t],
            [y3t]
        ])

    A += np.eye(A.shape[0]) * 1e-10
    
    try:
        # A^-1 @ b
        solutions = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        # the matrix isn't invertible
        A += np.eye(A.shape[0]) * 1e-10 # add SMALL value to matrix to make it invertible
        solutions = np.linalg.solve(A, b)

    # homogenize the matrix
    solutions = np.append(solutions, [[1.0]], axis = 0)

    # reshape homography to 3x3 matrix
    homography = np.reshape(solutions, (3,3))
    
    return np.asarray(homography)



def interpolate(image: np.ndarray, x: float, y: float) -> float | int:
    
    h, w, _ = image.shape

    # get neighboring points
    # clip to w/in bounds if necessary
    x0 = max(int(np.floor(x)), 0)
    y0 = max(int(np.floor(y)), 0)
    x1 = min(x0 + 1, w - 1) 
    y1 = min(y0 + 1, h - 1)

    # distances/weights between TL pixel and orginal pixel
    xw = x - x0
    yw = y - y0

    # neighboring pixel values
    p00 = image[y0, x0].astype(np.float32) # TL
    p01 = image[y0, x1].astype(np.float32) # TR
    p10 = image[y1, x0].astype(np.float32) # BL
    p11 = image[y1, x1].astype(np.float32) # BR

    return ( 
        p00 * (1 - xw) * (1 - yw) + 
        p01 * xw * (1 - yw) + 
        p10 * (1 - xw) * yw + 
        p11 * xw * yw
    )



def compose(source: np.ndarray, target: np.ndarray, transform: np.ndarray) -> np.ndarray:
    
    # dimension grabbing
    h, w, _ = source.shape
    target_h, target_w, _ = target.shape

    result = np.zeros_like(target)
    
    # invert transformation matrix for backward mapping
    transform_inv = np.linalg.inv(transform)

    for y in range(target_h):
        for x in range(target_w):
            
            # homogenize
            # aka add one dimension
            xy_target_homogenized = np.array([x, y, 1]) # (x, y) to (x, y, 1)

            # backward mapping
            xy_backward_map = transform_inv @ xy_target_homogenized.T # convert to column vector by using "T"
            xy_backward_map = np.array(xy_backward_map).flatten() # convert to 1d array

            # homogenous divide to get source coordinates
            x_source = xy_backward_map[0] / xy_backward_map[2]
            y_source  = xy_backward_map[1] / xy_backward_map[2]

            # just another classic boundary check
            if 0 <= x_source < w and 0 <= y_source < h: # we can siimply discard anything not in bounds

                result[y, x] = interpolate(source, x_source, y_source)

    return result