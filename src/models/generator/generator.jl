module Generateors

import .PieceWiseProductions: PieceWiseProduction

struct Generator
    id_::String
    is_unit_on_t0::Bool
    is_renewable::Bool

    start_up_cost_by_category::Dict{Int,Float64}
    piecewise_productions::Array{PieceWiseProduction}

    # 最小稼働時間
    time_up_minimum::Int
    # 最小再稼働時間, 停止したら次の稼働にはこの時間だけかかる
    time_down_minimum::Int

    power_output_minimum::Float64
    power_output_maximum::Float64


    # 開始時における稼働/停止時間/出力
    time_up_t0::Int
    time_down_t0::Int

end
end
