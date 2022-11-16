#print("\n".join(f"{i}{' '*(i-(int(__import__('math').log(i,10))))}{'e'*i}" for i in range(1, 101)))

s = 10
print("\n".join("\n".join(f"{' '*i}{'e'*i}" for i in range(1,s)) + "\n" + "\n".join(f"{' '*i}{'e'*i}" for i in range(s-1, 0, -1)) for i in range(5)))


#print("\n".join(round(amp * (m.sin((1 / x_scale) * i + m.pi)) + amp) * " " + w + ((round(amp * (m.sin((1 / x_scale) * i)) + round(amp * (m.sin((1 / x_scale) * i)) + amp))) * " " + w if (round(amp * (m.sin((1 / x_scale) * i)) + round(amp * (m.sin((1 / x_scale) * i)) + amp)) > 0) else w[abs(round(amp * (m.sin((1 / x_scale) * i)) + round(amp * (m.sin((1 / x_scale) * i)) + amp))):4] ) for i in [j for j in range(int(level * 2 * m.pi * x_scale))]))