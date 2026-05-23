# 1 1 2 5 6 7 10
def combinationSum2_naive(candidates: list[int], target: int) -> list[list[int]]:
    freq_map: dict[int, int] = dict()
    for cand in candidates:
        if cand not in freq_map:
            freq_map[cand] = 1
        else:
            freq_map[cand] += 1
    mask_list = []
    offset = 0

    for cand, freq in freq_map.items():
        bits = freq.bit_length()
        mask = ((1 << bits) - 1) << offset
        mask_list.append((offset, cand, mask))
        offset += bits

    # queue of (freq_encoded combo, intermediate target)
    queue = [(0, target)]
    grid: dict[int, set[int]] = {i: set() for i in range(target + 1)}
    while len(queue) != 0:
        combo, prev_target = queue.pop()

        # already dealt with this problem before, so move on
        if combo in grid[prev_target]:
            continue

        grid[prev_target].add(combo)
        for offset, cand, mask in mask_list:
            # get the count of the current candidate from the combo
            count = (combo & mask) >> offset

            # already used up all instances of this candidate
            if count == freq_map[cand]:
                continue

            next_target = prev_target - cand

            # overshot the target, so there's no viable combo that works
            if next_target < 0:
                continue

            incremented_count = count + 1
            # store the incremented count back into the combo
            next_combo = (combo & ~mask) | (incremented_count << offset)

            if next_target > 0:
                queue.append((next_combo, next_target))
            else:
                # we've already solved this problem, so we can just mark it as solved rather than enqueue it
                grid[next_target].add(next_combo)

    # convert combos back into actual lists
    total_list = []
    # grid[0] has the set of all unique combos that combine to the target
    # these combos are currently encoded, so we need to decode them
    for combo in grid[0]:
        nums = []
        for offset, cand, mask in mask_list:
            chosen_freq = (combo & mask) >> offset
            nums.extend([cand for i in range(chosen_freq)])
        total_list.append(nums)

    return total_list


def combinationSum2_sorted(candidates: list[int], target: int) -> list[list[int]]:
    num_cands = len(candidates)
    candidates.sort()

    queue: list[tuple[int, int, list[int]]] = [(0, target, [])]
    final_list = []

    while len(queue) != 0:
        start, cur_target, cur_chosen = queue.pop(0)
        cur_cand = -1

        for i in range(start, num_cands):
            if candidates[i] == cur_cand:
                continue
            cur_cand = candidates[i]

            new_target = cur_target - cur_cand
            if new_target < 0:
                break
            if new_target == 0:
                final_list.append(cur_chosen + [cur_cand])
                break
            elif new_target > 0 and i + 1 < num_cands:
                queue.append((i + 1, new_target, cur_chosen + [cur_cand]))

    return final_list
