import collections


def accountsMerge(accounts):
    emails = collections.defaultdict(list)
    res = []
    for idx, a in enumerate(accounts):
        for e in a[1:]:
            emails[e].append(idx)

    dupes = [val for val in emails.values() if len(val) > 1]

    for d in dupes:
        # each d is a list of indexes that have matching emails
        # use the FIRST dupe index as the final one
        to_merge_into = accounts[d[0]]
        root_emails = set(to_merge_into[1:])
        for id in d[1:]:
            more_emails = accounts[id][1:]
            root_emails.update(more_emails)
        full_emails = list(root_emails)
        full_emails.sort()
        for e in full_emails:
            if e in emails:
                del emails[e]
        full_emails.insert(0, to_merge_into[0])
        res.append(full_emails)

    remaining = [v[0] for v in emails.values()]

    for idx in set(remaining):
        # these will SINGLE email addresses that AREn't part of duplicate accounts
        singleton_account = accounts[idx]
        sorted_emails = sorted(singleton_account[1:])
        final = [singleton_account[0]]
        final.extend(sorted_emails)
        res.append(final)

    return res


test_accounts_1 = [["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John",
                                                                             "johnsmith@mail.com", "john00@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
test_accounts_2 = [["Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"], ["Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"], ["Ethan", "Ethan5@m.co",
                                                                                                                                "Ethan4@m.co", "Ethan0@m.co"], ["Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"], ["Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"]]
print(accountsMerge(test_accounts_2))
