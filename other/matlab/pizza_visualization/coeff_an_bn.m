% formula from Fulford & Blake (1986)

function [an,bn] = coeff_an_bn(sval)
global A B N0

M0 = 3;
an = zeros(7,2);
bn = zeros(6,2);
for n = 1 : N0+1
    for m = 1 : M0
        an(n,1) = an(n,1) +  A(m,n,1) * (sval^m);
        an(n,2) = an(n,2) +  A(m,n,2) * (sval^m);
    end
end

for n = 2 : N0+1
    for m = 1 : M0
        bn(n-1,1) = bn(n-1,1) +  B(m,n-1,1) * (sval^m);
        bn(n-1,2) = bn(n-1,2) +  B(m,n-1,2) * (sval^m);
    end
end

end