`timescale 1 ps/1 ps
`define OK 12
`define INCORRECT 13


module stimulus_gen (
	input clk,
	output logic reset,
	output logic s, w,
	input tb_match
);

	bit spulse_fail = 0;
	bit failed = 0;
	
	always @(posedge clk, negedge clk)
		if (!tb_match) failed = 1;
		
		
	initial begin
		reset <= 1;
		s <= 0;
		w <= 0;
		@(posedge clk);
		@(posedge clk);
		reset <= 0;
		@(posedge clk);
		@(posedge clk);
		
		s <= 1;

		repeat(200) @(posedge clk, negedge clk) begin
			w <= $random;
		end

		reset <= 1;
		@(posedge clk);
		reset <= 0;
		@(posedge clk);
		@(posedge clk);

		repeat(200) @(posedge clk, negedge clk) begin
			w <= $random;
		end
		
		@(posedge clk)		
			spulse_fail <= failed;
		
		repeat(500) @(posedge clk, negedge clk) begin
			reset <= !($random & 63);
			s <= !($random & 7);
			w <= $random;
		end

		if (failed && !spulse_fail) begin
			$display ("Hint: Your state machine should ignore input 's' after the state A to B transition.");
		end
		
		#1 $finish;
	end
	
endmodule

module tb();

	typedef struct packed {
		int errors;
		int errortime;
		int errors_z;
		int errortime_z;

		int clocks;
	} stats;
	
	stats stats1;
	
	
	wire[511:0] wavedrom_title;
	wire wavedrom_enable;
	int wavedrom_hide_after_time;
	
	reg clk=0;
	initial forever
		#5 clk = ~clk;

	logic reset;
	logic s;
	logic w;
	logic z_ref;
	logic z_dut;

	initial begin 
		$dumpfile("wave.vcd");
		$dumpvars(1, stim1.clk, tb_mismatch ,clk,reset,s,w,z_ref,z_dut );
	end


	wire tb_match;		// Verification
	wire tb_mismatch = ~tb_match;
	
	stimulus_gen stim1 (
		.clk,
		.* ,
		.reset,
		.s,
		.w );
	reference_module good1 (
		.clk,
		.reset,
		.s,
		.w,
		.z(z_ref) );
		
	TopModule top_module1 (
		.clk,
		.reset,
		.s,
		.w,
		.z(z_dut) );

	
	bit strobe = 0;
	task wait_for_end_of_timestep;
		repeat(5) begin
			strobe <= !strobe;  // Try to delay until the very end of the time step.
			@(strobe);
		end
	endtask	

	
	final begin
		if (stats1.errors_z) $display("Hint: Output '%s' has %0d mismatches. First mismatch occurred at time %0d.", "z", stats1.errors_z, stats1.errortime_z);
		else $display("Hint: Output '%s' has no mismatches.", "z");

		$display("Hint: Total mismatched samples is %1d out of %1d samples\n", stats1.errors, stats1.clocks);
		$display("Simulation finished at %0d ps", $time);
		$display("Mismatches: %1d in %1d samples", stats1.errors, stats1.clocks);
	end
	
	// Verification: XORs on the right makes any X in good_vector match anything, but X in dut_vector will only match X.
	assign tb_match = ( { z_ref } === ( { z_ref } ^ { z_dut } ^ { z_ref } ) );
	// Use explicit sensitivity list here. @(*) causes NetProc::nex_input() to be called when trying to compute
	// the sensitivity list of the @(strobe) process, which isn't implemented.
	always @(posedge clk, negedge clk) begin

		stats1.clocks++;
		if (!tb_match) begin
			if (stats1.errors == 0) stats1.errortime = $time;
			stats1.errors++;
		end
		if (z_ref !== ( z_ref ^ z_dut ^ z_ref ))
		begin if (stats1.errors_z == 0) stats1.errortime_z = $time;
			stats1.errors_z = stats1.errors_z+1'b1; end

	end
endmodule