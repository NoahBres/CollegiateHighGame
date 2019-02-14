def remap(x, min_in, max_in, min_out, max_out):
    return (x - min_in) * (max_out - min_out) / (max_in - min_in) + min_out


def limit_vec(vec, max):
    if vec.length() <= max:
        return

    vec.scale_to_length(max)
