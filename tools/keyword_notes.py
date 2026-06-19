from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    context_url: str
    note: str
    created_at: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "context_url": self.context_url,
            "note": self.note,
            "created_at": self.created_at,
            "tags": self.tags,
        }

    def pretty_print(self, indent: int = 0) -> str:
        prefix = " " * indent
        lines = [
            f"{prefix}Keyword: {self.keyword}",
            f"{prefix}URL:     {self.context_url}",
            f"{prefix}Note:    {self.note}",
            f"{prefix}Created: {self.created_at}",
        ]
        if self.tags:
            tags_str = ", ".join(self.tags)
            lines.append(f"{prefix}Tags:    {tags_str}")
        return "\n".join(lines)


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if any(t.lower() == tag.lower() for t in n.tags)]

    def format_all(self, separator: str = "\n---\n") -> str:
        parts = [note.pretty_print() for note in self.notes]
        return separator.join(parts)

    def summary(self) -> str:
        tag_count = {}
        for note in self.notes:
            for tag in note.tags:
                tag_count[tag] = tag_count.get(tag, 0) + 1
        return f"Total notes: {len(self.notes)}\nTags: {tag_count}"


def create_demo_collection() -> KeywordNoteCollection:
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword="乐鱼体育",
        context_url="https://portal-home-leyu.com.cn",
        note="这是一个体育相关的示例关键词，用于演示笔记功能。",
        tags=["体育", "示例"],
    )

    note2 = KeywordNote(
        keyword="乐鱼体育 会员",
        context_url="https://portal-home-leyu.com.cn/members",
        note="会员相关功能说明和常见问题解答。",
        tags=["会员", "FAQ"],
    )

    note3 = KeywordNote(
        keyword="乐鱼体育 活动",
        context_url="https://portal-home-leyu.com.cn/events",
        note="近期活动汇总，包括赛事预告和促销信息。",
        tags=["活动", "赛事"],
    )

    collection.add(note1)
    collection.add(note2)
    collection.add(note3)
    return collection


def main():
    collection = create_demo_collection()
    print("=== 全部笔记 ===")
    print(collection.format_all())

    print("\n=== 搜索 '会员' ===")
    for note in collection.find_by_keyword("会员"):
        print(note.pretty_print(indent=2))

    print("\n=== 搜索标签 '体育' ===")
    for note in collection.find_by_tag("体育"):
        print(note.pretty_print(indent=2))

    print("\n=== 统计 ===")
    print(collection.summary())


if __name__ == "__main__":
    main()