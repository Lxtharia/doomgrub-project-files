
struct chix
    a::Int16
end


struct data

end


t = chix(381)

print(reinterpret(Vector{Int8}, t))
