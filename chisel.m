r = 1.0
x = -r:0.01:r;

g = 25
a = 45
h = -1.5
t = 10

hold on

# circle
y = sqrt(power(r, 2) - power(x, 2))
plot (x, y);
plot (x, -y);

# tangent
x = 0:0.01:3;
m = -cot(g * pi / 180)
c = r / sin(g * pi / 180)
y =  m * x + c
plot (x, y);

# chisel
x = 0:0.01:3;
m = -cot((g + a) * pi / 180) 
c = r * sin(g * pi / 180) - m * r * cos(g * pi / 180)
y = m * x + c
plot (x, y);

# find l
g = 0:0.01:pi/2

m = -cot((g + a) .* pi / 180) 
c = r .* sin(g .* pi / 180) - m .* r .* cos(g .* pi / 180)
xt = (h - c) ./ m

xr = cos(g)
yr = sin(g)

l = sqrt(power(xt - xr, 2) + power(h - yr, 2))
lmin = l - t
[M, I] = min(abs(lmin))
M
I

ylim([-3 3])
xlim([-3 3])
hold off