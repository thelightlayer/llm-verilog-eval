module reference_module (
	input clock,
	input a, 
	output reg p,
	output reg q
);

	always @(negedge clock)
		q <= a;
		
	always @(*)
		if (clock)
			p = a;
endmodule
