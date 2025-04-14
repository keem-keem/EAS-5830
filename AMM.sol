// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/access/AccessControl.sol"; //This allows role-based access control through _grantRole() and the modifier onlyRole
import "@openzeppelin/contracts/token/ERC20/ERC20.sol"; //This contract needs to interact with ERC20 tokens
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;

contract AMM is AccessControl{
    bytes32 public constant LP_ROLE = keccak256("LP_ROLE");
	uint256 public invariant;
	address public tokenA;
	address public tokenB;
	uint256 feebps = 3; //The fee in basis points (i.e., the fee should be feebps/10000)

	event Swap( address indexed _inToken, address indexed _outToken, uint256 inAmt, uint256 outAmt );
	event LiquidityProvision( address indexed _from, uint256 AQty, uint256 BQty );
	event Withdrawal( address indexed _from, address indexed recipient, uint256 AQty, uint256 BQty );

	/*
		Constructor sets the addresses of the two tokens
	*/
    constructor( address _tokenA, address _tokenB ) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender );
        _grantRole(LP_ROLE, msg.sender);

		require( _tokenA != address(0), 'Token address cannot be 0' );
		require( _tokenB != address(0), 'Token address cannot be 0' );
		require( _tokenA != _tokenB, 'Tokens cannot be the same' );
		tokenA = _tokenA;
		tokenB = _tokenB;

    }


	function getTokenAddress( uint256 index ) public view returns(address) {
		require( index < 2, 'Only two tokens' );
		if( index == 0 ) {
			return tokenA;
		} else {
			return tokenB;
		}
	}

	/*
		The main trading functions
		
		User provides sellToken and sellAmount

		The contract must calculate buyAmount using the formula:
	*/
	function tradeTokens( address sellToken, uint256 sellAmount ) public {
		require( invariant > 0, 'Invariant must be nonzero' );
		require( sellToken == tokenA || sellToken == tokenB, 'Invalid token' );
		require( sellAmount > 0, 'Cannot trade 0' );
		require( invariant > 0, 'No liquidity' );
		require(IERC20(sellToken).transferFrom(msg.sender, address(this), sellAmount), "Token transfer failed");

		uint256 qtyA;
		uint256 qtyB;
		uint256 swapAmt;

		//YOUR CODE HERE

		address buyToken = sellToken == tokenA ? tokenB : tokenA;

		uint256 balanceSellBefore = IERC20(sellToken).balanceOf(address(this));
		uint256 balanceBuy = IERC20(buyToken).balanceOf(address(this));

		// Pull in the sold tokens (user must approve first)
		IERC20(sellToken).transferFrom(msg.sender, address(this), sellAmount);

		uint256 balanceSellAfter = IERC20(sellToken).balanceOf(address(this));
		uint256 actualIn = balanceSellAfter - balanceSellBefore;

		// Apply fee
		uint256 effectiveIn = (actualIn * (10000 - feebps)) / 10000;

		// Calculate how many buy tokens to return (x * y = k)
		uint256 newBalanceSell = balanceSellAfter;
		uint256 newBalanceBuy = invariant / newBalanceSell;
		uint256 amountOut = balanceBuy - newBalanceBuy;

		require(amountOut > 0, "Output too low");

		IERC20(buyToken).transfer(msg.sender, amountOut);

		emit Swap(sellToken, buyToken, actualIn, amountOut);


		uint256 new_invariant = IERC20(tokenA).balanceOf(address(this))*IERC20(tokenB).balanceOf(address(this));
		require( new_invariant >= invariant, 'Bad trade' );
		invariant = new_invariant;
	}

	/*
		Use the ERC20 transferFrom to "pull" amtA of tokenA and amtB of tokenB from the sender
	*/
	function provideLiquidity( uint256 amtA, uint256 amtB ) public {
		require( amtA > 0 || amtB > 0, 'Cannot provide 0 liquidity' );
		//YOUR CODE HERE

		require(amtA > 0 || amtB > 0, 'Cannot provide 0 liquidity');

    		require(IERC20(tokenA).safeTransferFrom(msg.sender, address(this), amtA), "Token A transfer failed");
    		require(IERC20(tokenB).safeTransferFrom(msg.sender, address(this), amtB), "Token B transfer failed");

    		invariant = IERC20(tokenA).balanceOf(address(this)) * IERC20(tokenB).balanceOf(address(this));

		emit LiquidityProvision( msg.sender, amtA, amtB );
	}

	/*
		Use the ERC20 transfer function to send amtA of tokenA and amtB of tokenB to the target recipient
		The modifier onlyRole(LP_ROLE) 
	*/
	function withdrawLiquidity( address recipient, uint256 amtA, uint256 amtB ) public onlyRole(LP_ROLE) {
		require( amtA > 0 || amtB > 0, 'Cannot withdraw 0' );
		require( recipient != address(0), 'Cannot withdraw to 0 address' );
		if( amtA > 0 ) {
			IERC20(tokenA).safeTransferFrom(recipient,amtA);
		}
		if( amtB > 0 ) {
			IERC20(tokenB).safeTransferFrom(recipient,amtB);
		}
		invariant = IERC20(tokenA).balanceOf(address(this))*IERC20(tokenB).balanceOf(address(this));
		emit Withdrawal( msg.sender, recipient, amtA, amtB );
	}


}
