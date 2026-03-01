def to_dot(nodes: list[tuple[str, list[str]]]) -> str:
    lines = ["digraph bayaml {"]
    for node, deps in nodes:
        if not deps:
            lines.append(f'  "{node}";')
        for dep in deps:
            lines.append(f'  "{dep}" -> "{node}";')
    lines.append("}")
    return "\n".join(lines)
