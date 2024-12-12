import queue


class Solution:
    def findOrder(self, numCourses, prerequisites):
        edges = {i: [] for i in range(numCourses)}
        degrees = [0 for i in range(numCourses)]
        for i, j in prerequisites:
            edges[j].append(i)
            degrees[i] += 1
        q = queue.Queue(maxsize=numCourses)

        for i in range(numCourses):
            if degrees[i] == 0:
                q.put(i)

        order = []
        while not q.empty():
            node = q.get()
            order.append(node)

            for x in edges[node]:
                degrees[x] -= 1
                if degrees[x] == 0:
                    q.put(x)

        if len(order) == numCourses:
            return order
        return []
