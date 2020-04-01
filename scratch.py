from data_utils import *

# args = get_args(sys.argv[1:])
# np.random.seed(args.seed)
# total_images, total_labels = load_data(args)
# sample_size = args.sample_size
# imgs = total_images[np.random.choice(range(len(total_images)), size = sample_size, replace = False)]
# estimate_sigma(imgs)

naive_dcs = np.array([1470000, 12000000, 75000000, 300000000])
ucb_dcs = np.array([1830100, 8592900, 31967900])

# naive_times = np.array([14.201, 122.213, 122.213])
# ucb_times = np.array([22.277, 101.315, 101.315])

x = np.arange(500, 10100, 100)
quadratic =  3*(x**2)
knlogn = 2.5e2*3*(x*np.log(x))

plt.plot([700, 2000, 5000, 10000], naive_dcs, 'bo')
plt.plot([700, 2000, 5000], ucb_dcs, 'ro')
plt.plot(x, quadratic, 'b-')
plt.plot(x, knlogn, 'r-')
plt.show()

#
# plt.plot([700, 2000, 5000], naive_times)
# plt.plot([700, 2000, 5000], ucb_times)
# plt.show()
