function cilia = cilia_position(i,j,time)
global N_element d_element phi root_position L_element sigma d1_cilia d2_cilia N0

root_position = [i * d1_cilia, j * d2_cilia, 0];
position = zeros(N_element(i,j),3);
cilia = zeros(N_element(i,j),3);
for s = 1 : N_element(i,j)
    sval = d_element*(s-0.5)/L_element(i,j);
    [an,bn] = coeff_an_bn(sval);
    position(s,1) = 0.5 .* an(1,1);
    position(s,3) = 0.5 .* an(1,2);
    for n = 1 : N0
        position(s,1) = position(s,1) + an(n+1,1) * cos(n*(sigma*time+phi*i)) + bn(n,1) * sin(n*(sigma*time+phi*i));
        position(s,3) = position(s,3) + an(n+1,2) * cos(n*(sigma*time+phi*i)) + bn(n,2) * sin(n*(sigma*time+phi*i));
    end
    cilia(s,:) = root_position + L_element(i,j) .* position(s,:);
end