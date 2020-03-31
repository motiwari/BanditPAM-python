from data_utils import *


def UCB_build(args, imgs):
    # When to stop sampling an arm? Ans: When lcb >= ucb_1
    # How to determine sigma? Ans: Seems to be determined manually by looking at distribution of data. Confidence bound scales as sigma (makes sense)

    ### Parameters
    N = len(imgs)
    p = 1e-2
    sigma = 0.7
    num_samples = np.zeros(N)
    estimates = np.zeros(N)
    medoids = []
    best_distances = [float('inf') for _ in range(N)]
    batch_size = 100 # NOTE: What should this init_size be? 20? Also note that this will result in (very minor) inefficiencies when batch_size > 1

    def sample_for_targets(imgs, targets, batch_size):
        # NOTE: Fix this with array broadcasting
        N = len(imgs)
        estimates = np.zeros(len(targets))
        tmp_refs = np.array(np.random.choice(N, size = batch_size, replace = False), dtype='int')
        for tar_idx, target in enumerate(targets):
            distances = np.zeros(batch_size)
            for tmp_idx, tmp in enumerate(tmp_refs):
                ## tmp is the actually index of the reference point, tmp_idx just numerates them)
                distances[tmp_idx] = cost_fn(imgs, target, tmp, best_distances) # NOTE: depends on other medoids too!
            estimates[tar_idx] = np.mean(distances)
        return estimates

    # Iteratively:
    # Pretend each previous arm is fixed.
    # For new arm candidate, true parameter is the TRUE loss when using the point as medoid
        # As a substitute, can measure the "gain" of using this point -- negative DECREASE in distance (the lower the distance, the better)
    # We sample this using UCB algorithm to get confidence bounds on what that loss will be
    # Update ucb, lcb, and empirical estimate by sampling WITH REPLACEMENT(NOTE)
        # If more than n points, just compute exactly -- otherwise, there's a failure mode where
        # Two points very close together require shittons of samples to distinguish their mean distance

    for k in range(args.num_medoids):
        print("Finding medoid", k)
        ## Initialization
        step_count = 0
        candidates = range(N)
        lcbs = -100 * np.ones(N)
        ucbs = -100 * np.ones(N)

        # Pull arms, update ucbs and lcbs
        while(len(candidates) > 1): # NOTE: Should also probably restrict absolute distance in cb_delta?
            print("Step count", step_count, candidates)
            step_count += 1
            # NOTE: Don't update all estimates, just pulled arms
            estimates[candidates] = (((step_count - 1) * estimates[candidates]) + sample_for_targets(imgs, candidates, batch_size)) / step_count
            cb_delta = sigma * np.sqrt(np.log(1 / p) / (batch_size * step_count))
            lcbs[candidates] = estimates[candidates] - cb_delta
            ucbs[candidates] = estimates[candidates] + cb_delta

            # Determine arms to pull
            best_ucb = ucbs.min()
            candidates = np.where(lcbs < best_ucb)[0]
        print("Medoid:", candidates)
        medoids.append(candidates[0])
        best_distances = get_best_distances(medoids, imgs)
    print(medoids)
