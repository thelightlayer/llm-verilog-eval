module reference_module (
	input [7:0] in,
	output parity
);

	assign parity = ^in;
	
endmodule
