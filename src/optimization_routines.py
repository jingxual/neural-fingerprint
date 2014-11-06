import numpy as np
import numpy.random as npr

def sgd_with_momentum(grad, N_x, N_w, callback=None,
                      batch_size=100, num_epochs=100, learn_rate=0.1,
                      momentum=0.9, param_scale=0.1, **kwargs):
    w = npr.randn(N_w) * param_scale
    cur_dir = np.zeros(N_w)
    batches = batch_idx_generator(batch_size, N_x)
    for epoch in xrange(num_epochs):
        for batch in batches:
            cur_grad = grad(batch, w)
            cur_dir = momentum * cur_dir - (1.0 - momentum) * cur_grad
            w += learn_rate * cur_dir
        if callback: callback(epoch, w)
    return w

def rms_prop(grad, N_x, N_w, callback=None,
             batch_size=100, num_epochs=100, learn_rate=0.1,
             param_scale=0.1, gamma=0.9, **kwargs):
    w = npr.randn(N_w) * param_scale
    avg_sq_grad = np.ones(N_w)
    batches = batch_idx_generator(batch_size, N_x)
    for epoch in xrange(num_epochs):
        for batch in batches:
            cur_grad = grad(batch, w)
            avg_sq_grad = avg_sq_grad * gamma + cur_grad**2 * (1 - gamma)
            w -= learn_rate * cur_grad/np.sqrt(avg_sq_grad)
        if callback: callback(epoch, w)
    return w

def sgd_nesterov_momentum(grad, N_x, N_w, callback=None,
             batch_size=100, num_epochs=100, learn_rate=0.1,
             param_scale=0.1):
    # TODO
    pass

def make_batcher(input_data, batch_size):
    batch_idxs = batch_idx_generator(batch_size, len(input_data.values()[0]))
    data_batches = [{k : v[idxs] for k, v in input_data.iteritems()}
                    for idxs in batch_idxs]
    def batcher():
        for data_batch in data_batches:
            for node, value in data_batch.iteritems():
                node.value = value
            yield

    return batcher

def batch_idx_generator(batch_size, total_size):
    start = 0
    end = batch_size
    batches = []
    while True:
        if start >= total_size:
            break
        batches.append(slice(start, end))
        start += batch_size
        end += batch_size

    return batches
