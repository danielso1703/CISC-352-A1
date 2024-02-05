import itertools


domains = [x for (x) in itertools.product(range(1, 10), repeat=3)]
mod_domain = []
for domain in domains:
    if len(set(domain)) == len(domain):
        mod_domain.append(domain)
print(mod_domain)