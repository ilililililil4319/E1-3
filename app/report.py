"""결과 요약: 전체/통과/실패 수와 실패 케이스 목록 (요구사항 9)."""


class Summary:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failures = []   # [(케이스 이름, 실패 이유), ...]

    def add_pass(self):
        self.total += 1
        self.passed += 1

    def add_fail(self, case_id, reason):
        self.total += 1
        self.failures.append((case_id, reason))

    @property
    def failed(self):
        return len(self.failures)

    def lines(self):
        out = [
            "총 테스트: {}개".format(self.total),
            "통과: {}개".format(self.passed),
            "실패: {}개".format(self.failed),
        ]
        if self.failures:
            out.append("실패 케이스:")
            for case_id, reason in self.failures:
                out.append("- {}: {}".format(case_id, reason))
        return out
