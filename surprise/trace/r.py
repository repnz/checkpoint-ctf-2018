variables = \
{
	'main12_' : 'length_of_fields',
	'main11_' : 'fields',
	'main9_' : 'user_input',
	'main48_' : 'fields_i',
	'main17_' : 'current_int_field',
	'main13_' : 'fields_num',
	'main51_' : 'current_num',
	'nas6_' : 'len_of_a',
	'nas7_' : 'len_of_a_min_1',
	'nas14_': 'loop_var',
	'nas28_' : 'loop_var_min_1',
	'nas8_' : 'current_a_char',
	'nas9_' : 'current_a_digit',
	'nas10_': 'int_current_a_digit',
	'nas12_' : 'z',
	'nas5_' : 'new_outut_arr',
	'doom6_' : 'aa_length_min_1',
	'doom21_' : 'old_loop_var',
	'doom17_' : 'i',
	'andre0_' : 'length_of_a',
	'andre1_' : 'length_of_b',
	'andre12_': 'length_of_a_again',
	'andre11_': 'length_of_10',
	'andre35_': 'new_b_i',
	'andre22_': 'b_i',
	'andre23_': 'length_of_b',
	'andre37_': 'length_of_a',
	'andre36_': 'a_i',
	'andre26_': 'a_val',
	'andre28_': 'b_val',
	'andre34_': 'new_a_i',
	'andre40_': 'andre10_i',
	'andre45_': 'i_plus_one',
	'andre46_': 't10_i_plus_one_addr',
	'andre50_': 't10_i_1',
	'andre48_': 't10_i_val',
	'rakim5_': 'diff_arr',
	'rakim8_': 'i',
	'rakim28_': 'new_i',
	'rakim12_': 'a_i_val',
	'rakim17_': 'b_i_val',
	'rakim13_': 'a_i',
	'rakim18_': 'b_i',
	'gza4_': 'return_list_value',
	'gza11_': 'len_of_return_list',
	'gza14_': 'i',
	'gza13_': 'old_i',
	'gza12_': 'wu',
	'gza16_': 'len_of_a',
	'gza19_': 'a_i_val',
	'gza20_': 'a_i',
	'gza24_': 'b_i_val',
	'gza25_': 'b_i',
	'gza28_': 'new_wu',
	'gza27_': 'sum_of_digits',
	'gza31_': 's_of_digits',
	'main60_': 'length_of_fields_num',
	'main59_': 'fields_num_i',
	'main54_': 'current_field_num_1',
	'main62_': 'next_field_num_1',
	'main57_': 'half_fields_num_length',
	'main58_': 'half_fields_arr',
	'main74_': 'half_fields_num_length',
	'main73_': 'half_fields_num_i',
	'main72_': 'new_half_fields_num_i',
	'main63_': 'current_half_fields_num_ptr',
	'main64_': 'half_fields_num_i_m2',
	'main67_': 'half_fields_num_i_m2',
	'main68_': 'half_fields_num_i_m2p1',
	'main87_': 'len_of_half_fields_arr',
	'main86_': 'half_fields_arr_i',
	'main89_': 'next_i',
	'main78_': 'sum_until_now',
	'main79_': 'ascii_sum_until_now',
	'main80_': 'digits_sum_until_now',
	'main99_': 'o_su',
	'main96_': 'o_su',
	'main100_': 'e_su',
	'main92_': 'e_su',
	'main101_': 'i',
	'main97_': 'i',
	'main102_': 'len_of_fields_num',
	'main103_': 'len_of_fields_num_m_1',
	'main91_': 'current_num',
	'main108_' : 'u_arr',
	'main118_': 'u_arr',
	'main109_': 'i',
	'main117_': 'i',
	'main119_': 'x',
	'main128_': 'x',
	'doom14_': 'm',
	'doom15_': 'len_of_bb',
	'doom28_': 'i',
	'doom7_': 'ii',
	'doom3_': 'current_a',
	'doom5_': 'length_of_aa',
	'doom0_': 'len_of_aa',
	'doom1_': 'len_of_aa_div2',
	'doom10_': 'ii'

}

data = open('functions.ssa').read()

for var_name, var_new_name in variables.iteritems():
    data = data.replace(var_name, var_new_name)

open('functions.ssa', 'w').write(data)