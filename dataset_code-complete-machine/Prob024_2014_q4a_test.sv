`timescale 1 ps/1 ps
`define OK 12
`define INCORRECT 13


module stimulus_gen (
	input clk,
	output logic w, R, E, L
);

	initial begin
		repeat(200) @(posedge clk, negedge clk) begin
			{w,R,E,L} <= $random;
		end
		
		#1 $finish;
	end
	
endmodule

module tb();

	typedef struct packed {
		int errors;
		int errortime;
		int errors_Q;
		int errortime_Q;

		int clocks;
	} stats;
	
	stats stats1;
	
	
	wire[511:0] wavedrom_title;
	wire wavedrom_enable;
	int wavedrom_hide_after_time;
	
	reg clk=0;
	initial forever
		#5 clk = ~clk;

	logic w;
	logic R;
	logic E;
	logic L;
	logic Q_ref;
	logic Q_dut;

	initial begin 
		$dumpfile("wave.vcd");
		$dumpvars(1, stim1.clk, tb_mismatch ,clk,w,R,E,L,Q_ref,Q_dut );
	end


	wire tb_match;		// Verification
	wire tb_mismatch = ~tb_match;
	
	stimulus_gen stim1 (
		.clk,
		.* ,
		.w,
		.R,
		.E,
		.L );
	reference_module good1 (
		.clk,
		.w,
		.R,
		.E,
		.L,
		.Q(Q_ref) );
		
	TopModule top_module1 (
		.clk,
		.w,
		.R,
		.E,
		.L,
		.Q(Q_dut) );

	
	bit strobe = 0;
	task wait_for_end_of_timestep;
		repeat(5) begin
			strobe <= !strobe;  // Try to delay until the very end of the time step.
			@(strobe);
		end
	endtask	

	
	final begin
		if (stats1.errors_Q) $display("Hint: Output '%s' has %0d mismatches. First mismatch occurred at time %0d.", "Q", stats1.errors_Q, stats1.errortime_Q);
		else $display("Hint: Output '%s' has no mismatches.", "Q");

		$display("Hint: Total mismatched samples is %1d out of %1d samples\n", stats1.errors, stats1.clocks);
		$display("Simulation finished at %0d ps", $time);
		$display("Mismatches: %1d in %1d samples", stats1.errors, stats1.clocks);
	end
	
	// Verification: XORs on the right makes any X in good_vector match anything, but X in dut_vector will only match X.
	assign tb_match = ( { Q_ref } === ( { Q_ref } ^ { Q_dut } ^ { Q_ref } ) );
	// Use explicit sensitivity list here. @(*) causes NetProc::nex_input() to be called when trying to compute
	// the sensitivity list of the @(strobe) process, which isn't implemented.
	always @(posedge clk, negedge clk) begin

		stats1.clocks++;
		if (!tb_match) begin
			if (stats1.errors == 0) stats1.errortime = $time;
			stats1.errors++;
		end
		if (Q_ref !== ( Q_ref ^ Q_dut ^ Q_ref ))
		begin if (stats1.errors_Q == 0) stats1.errortime_Q = $time;
			stats1.errors_Q = stats1.errors_Q+1'b1; end

	end
endmodule